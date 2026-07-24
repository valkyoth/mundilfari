crate name: Mundilfari

> Historical design discussion. All earlier proposals for Mundilfari-owned
> GNSS/NMEA/receiver decoding are superseded by the final Navheim ownership
> addendum at the bottom of this document and
> [NAVHEIM_INTEGRATION.md](NAVHEIM_INTEGRATION.md).

I want you to make a extremely indepth technical architecture guide for a time protocol that will support every time protocol that exists in extreme depth. first make sure we really have every protocol that exists. second it must be the ultimate crate so it should have very easy to use apis that support everything you can do with a time protocol. Someone might want to make a clock, a linux app, a deamon, use it in their code, use it in their site whatever is possible do a good thinking pass on what someone would want to do with a time crate.

then make sure security is extremely important and that we always follow the official rfc standard if exist or documentation.

each protocol should become its own crate so mundilfari is the mean crate and for example mundilfare-time implements the time protocol, mundilfari-daytime implements the daytime protocol etc etc.

make it very in details and make versions so start with 0.1.0 and go up to how far you need to go even if it is 0.1000.0 for example we not care. but make sure everything is planned before 1.0.0 so that once we reach that each protocol is implemented and usable.

Original idea:
This design scales from parsing simple ASCII strings to managing raw Linux socket hardware timestamps, covering every official RFC and major IEEE standard.

The architecture is built on a modular crate structure where users can pull in just the protocol they need (e.g., timi-sntp), or use the umbrella crate (timi) for a unified, high-level facade.
1. Workspace Architecture & Philosophy

Design Tenets:

    no_std where possible: Protocol parsing/serialization crates must be #![no_std] compatible so they can run on embedded devices and microcontrollers.

    Separation of I/O from Logic: The core protocol crates should only handle state machines and byte buffering. Network execution (TCP/UDP/Raw sockets) is handled by optional std features or async runtimes (Tokio/async-std) via feature flags (e.g., features = ["tokio"]).

    Universal Time Type: All crates resolve to a standard internal timi_core::Timestamp which can easily convert to std::time::SystemTime or chrono::DateTime.

Workspace Tree
Plaintext

timi-workspace/
├── timi/                 # The umbrella facade crate
├── timi-core/            # Primitives, epochs, fractions, math
├── timi-icmp/            # RFC 792 (ICMP Timestamp)
├── timi-daytime/         # RFC 867 (Daytime)
├── timi-time/            # RFC 868 (TIME)
├── timi-sntp/            # RFC 5905 (SNTP)
├── timi-nmea/            # NMEA 0183 (GPS serial time)
├── timi-irig/            # IRIG-B (Timecode frames)
├── timi-ntp/             # RFC 5905 (Full daemon, clock slewing)
├── timi-nts/             # RFC 8915 (Network Time Security)
├── timi-roughtime/       # IETF Roughtime (Secure auth chains)
├── timi-ptp/             # IEEE 1588-2019 (Hardware timestamps)
└── timi-wr/              # White Rabbit PTP (CERN extension)

2. The Foundation: timi-core

Before handling any network data, you need a unified way to handle the chaotic world of time epochs.

    Unix Epoch: Jan 1, 1970

    NTP/TIME Epoch: Jan 1, 1900

    PTP/GPS Epoch: Jan 6, 1980 (and does not count leap seconds)

Core API (timi_core::Timestamp):
Rust

pub struct Timestamp {
    pub seconds: u64,
    pub fractional: u32, 
    pub epoch: TimeEpoch,
}

pub enum TimeEpoch { Unix, Ntp, Gps }

impl Timestamp {
    // Converts any protocol's native time into a standard Rust SystemTime
    pub fn to_system_time(&self) -> std::time::SystemTime { ... }
}

3. Tier 1: The Legacy & Primitives (🟢 Easy)

These protocols are strictly request-response, with no clock drift calculations or hardware dependencies.
timi-daytime (RFC 867 - Daytime Protocol)

    Mechanics: Connect to TCP/UDP port 13, read ASCII string, close.

    API Goal: Provide a simple timi_daytime::fetch() that returns a String.

    Challenge: Because RFC 867 doesn't strictly define the format (it can be Tuesday, October 1, 1985 20:14:21 or 01 OCT 1985 20:14), the crate needs a heuristic regex or fallback parser to turn it into a valid SystemTime.

timi-time (RFC 868 - TIME Protocol)

    Mechanics: Connect to TCP/UDP port 37, receive a 32-bit big-endian integer of seconds since 1900.

    API Goal: timi_time::Client::sync(&str) -> Result<Timestamp>

timi-icmp (RFC 792 - ICMP Timestamp)

    Mechanics: Operates at Layer 3 (IP). Sends ICMP Type 13 (Timestamp Request) and awaits ICMP Type 14 (Timestamp Reply).

    Precision: Milliseconds since midnight UTC.

    Architecture: Requires raw sockets (SOCK_RAW, IPPROTO_ICMP) because standard UDP/TCP sockets won't allow crafting ICMP headers. You will need elevated OS privileges (root/sudo) to execute this.

4. Tier 2: General Purpose & Hardware Serial (🟡 Moderate)

These are modern protocols heavily used in IT and embedded systems, but they still don't require altering the OS kernel clock directly.
timi-sntp (RFC 5905 - Simple Network Time Protocol)

    Mechanics: UDP port 123. Sends a 48-byte struct, receives a 48-byte struct.

    Architecture:

        Define SntpRequest and SntpResponse structs.

        Implement to_bytes() and from_bytes() using bitwise masking for the leap indicator, version, and mode fields.

        Compute network delay: Delay = (T4 - T1) - (T3 - T2).

        Compute offset: Offset = ((T2 - T1) + (T3 - T4)) / 2.

    API Goal: Extremely simple single-shot sync. timi_sntp::sync("pool.ntp.org")

timi-nmea (NMEA 0183)

    Mechanics: Parses GPS serial output over UART/USB (e.g., /dev/ttyUSB0).

    Architecture: Looks for sentences starting with $GPRMC (Recommended Minimum Specific GPS/Transit Data) or $GPZDA (Time & Date), verifies the XOR checksum at the end of the sentence, and extracts the UTC time.

timi-irig (IRIG-B Standard 200-04)

    Mechanics: Parses 100 pulses-per-second pulse-width modulated (PWM) audio/voltage streams.

    Architecture: A no_std state machine that consumes binary high/low states and durations, shifting bits into a 100-bit frame containing seconds, minutes, hours, days, and years.

5. Tier 3: Advanced Time Engines & Security (🟠 Hard)

Here, the library transitions from simply asking the time to maintaining the time over long durations securely.
timi-ntp (RFC 5905 - Full Network Time Protocol)

    Architecture:

        Requires a long-running background thread/daemon.

        Marzullo's Algorithm / Intersection: Queries 4+ servers, filters out "falsetickers" (lying servers), and averages the remainder.

        Phase-Locked Loop (PLL): Instead of stepping the clock (which breaks databases), it uses FFI to call libc::adjtimex() on Linux or SetSystemTimeAdjustment() on Windows to speed up or slow down the OS tick rate gracefully.

timi-nts (RFC 8915 - Network Time Security)

    Mechanics: Wraps NTP in cryptographic authentication.

    Architecture:

        Phase 1: NTS Key Exchange (NTS-KE) over TLS 1.3 (TCP port 4460) to obtain symmetric keys and AEAD cookies.

        Phase 2: Standard NTP (UDP 123) but with the NTS cookies appended as Extension Fields to validate the server's identity cryptographically. Requires a dependency on rustls.

timi-roughtime (IETF Draft / Google)

    Architecture: A pure Rust implementation of the Roughtime protocol. The client sends a random nonce. The server replies with a cryptographic signature binding the time, the client's nonce, and a Merkle tree root of other clients' recent requests, ensuring the server cannot lie without providing mathematical proof of its lie.

6. Tier 4: The Hardware / Sub-Microsecond Layer (🔴 Extreme)

At this tier, standard OS sockets are entirely bypassed. You are writing Rust code that communicates directly with Network Interface Card (NIC) drivers.
timi-ptp (IEEE 1588-2019 - Precision Time Protocol)

    Mechanics: Achieves nanosecond accuracy by timestamping packets exactly as they leave the physical silicon of the ethernet port.

    Architecture:

        Layer 2 Sockets: Bypasses IP entirely using AF_PACKET and SOCK_RAW with EtherType 0x88F7.

        Ancillary Data (cmsg): Uses low-level recvmsg and sendmsg syscalls to request SO_TIMESTAMPING data from the NIC.

        Hardware Clock Control: Interfaces with Linux PTP character devices (/dev/ptpX). Uses ioctl() to execute commands like PTP_CLOCK_GETTIMEX to slew the physical crystal oscillator on the network card.

timi-wr (White Rabbit PTP)

    Architecture: An extension of PTP used by CERN. It requires implementing Synchronous Ethernet (SyncE) payload processing to lock the physical layer frequency, parsing specialized WR-TLV (Type-Length-Value) extensions inside the PTP Announce messages.

7. The Umbrella Facade: timi

The true power of this workspace is the top-level timi crate. It hides all the RFC complexity behind a beautiful, unified Rust API for application developers.

A developer building a web app doesn't need to know how SNTP calculates root dispersion; they just want to know if their server clock is accurate.
Rust

use timi::{TimeClient, Protocol};

#[tokio::main]
async fn main() {
    // 1. The Easiest API in the world (defaults to SNTP over pool.ntp.org)
    let time = timi::now().await.unwrap();
    println!("True network time: {}", time);

    // 2. A flexible builder for full control
    let mut client = TimeClient::builder()
        .protocol(Protocol::Nts) // Use Secure NTP (RFC 8915)
        .add_server("time.cloudflare.com")
        .timeout(std::time::Duration::from_secs(2))
        .build();

    // Fetch the time and offset
    let sync_report = client.sync().await.unwrap();
    
    println!("My OS clock is off by {} milliseconds", sync_report.offset_ms);
    
    // 3. For Daemon/App makers: start a background sync task
    // This will gently slew the OS clock in the background
    timi::daemon::start_sync_engine(client).await;
}

Why this architecture wins:

By isolating the network layout, binary parsing, and OS-specific syscalls into distinct crates (timi-core, timi-sntp, etc.), you allow embedded developers to use timi-sntp on a Raspberry Pi Pico (using no_std), while cloud engineers can use the full timi umbrella crate with tokio to secure their distributed databases using NTS.
Worked for 5m 44s
to add it most be no_std where possible and no other crates can be used, it should be own implementation but ofcourse we need to use the linux kernel etc for certain parts so that is fine.
Worked for 13m 41s

The zero-dependency requirement makes Mundilfari substantially more ambitious than an ordinary protocol library. It becomes a complete time stack: arithmetic, calendars, time scales, wire codecs, cryptography, TLS 1.3, socket integration, hardware timestamping, clock discipline, protocol engines, servers, daemons, and conformance tooling—all implemented inside one Rust workspace.

Mundilfari
A zero-dependency, security-first, no_std-first time protocol framework for Rust

Planned stability target: 1.0.0
Protocol baseline date: 23 July 2026
Implementation language: Rust
External Rust dependencies: None
Default protocol-crate environment: #![no_std]
Primary targets: embedded systems, applications, servers, websites, operating-system daemons, time appliances, GNSS receivers, industrial equipment, PTP hardware, forensic tools, and protocol test systems.

1. Executive architecture decision

Mundilfari should not be designed merely as an NTP library with a few related decoders.

It should be designed as a complete framework for:

Representing time correctly.
Transferring time over networks and physical signals.
Authenticating time.
Estimating uncertainty.
Comparing multiple time sources.
Controlling software, system, hardware, and virtual clocks.
Parsing historical and current protocols.
Running time clients and servers.
Building Linux daemons.
Operating in embedded no_std environments.
Inspecting and generating protocol messages.
Producing trusted timestamp evidence.
Testing other time implementations.
Converting between epochs, scales, time zones, wire formats, and calendar representations.

The top-level mundilfari crate provides the unified API. Every independently standardized protocol or protocol family receives its own crate.

Examples:

mundilfari
mundilfari-core
mundilfari-daytime
mundilfari-time
mundilfari-icmp-time
mundilfari-sntp
mundilfari-ntp
mundilfari-nts
mundilfari-roughtime
mundilfari-ptp
mundilfari-gptp
mundilfari-white-rabbit
mundilfari-nmea0183
mundilfari-irig

The spelling must always be mundilfari, including crates such as mundilfari-time, rather than mundilfare-time.

2. What “every time protocol” can honestly mean

It is impossible to prove that a project supports literally every time protocol ever created. Some protocols are:

Proprietary and unpublished.
Available only under commercial standards licences.
Classified or limited to closed systems.
Specific to one discontinued device.
Informally defined by source code rather than a specification.
Still being drafted.
Unknown outside their original organization.
Merely custom register layouts rather than true protocols.

Mundilfari should therefore define a precise completeness contract.

2.1 The Mundilfari 1.0 completeness contract

Mundilfari 1.0.0 will cover:

Every publicly documented time-transfer, clock-synchronization, timecode, trusted-timestamp, time-discovery, and standardized time-representation protocol entered in the Mundilfari Protocol Registry by the baseline date.
Every relevant stable IETF RFC and incorporated update or verified erratum.
Major IEEE, IEC, ITU-T, SMPTE, CCSDS, GNSS, industrial, broadcast, radio, automotive, and IoT standards for which the project has obtained legitimate access to the normative specification.
Historical protocols where interoperable implementations or authoritative documents still exist.
Active drafts under explicitly versioned experimental APIs.
A vendor-extension system for documented but non-standard protocols.

Mundilfari will not claim implementation of an inaccessible protocol. The registry will instead mark it:

KnownUnavailable
LicenceRequired
SpecificationRequested
ImplementationBlocked
ProprietaryUndocumented
HistoricalEvidenceOnly

This is much more trustworthy than claiming universal coverage while silently guessing fields.

2.2 Standards status classes

Every protocol entry must have one of these statuses:

pub enum SpecificationStatus {
    StableNormative,
    StableInformational,
    ExperimentalRfc,
    ActiveDraft,
    Obsolete,
    Historic,
    VendorPublished,
    LicensedNormative,
    PartiallyDocumented,
    Unavailable,
}

Stable standards are covered by the stable API.

Draft protocols use version-pinned namespaces or features:

experimental-ntpv5-draft-09
experimental-roughtime-draft-19
experimental-nts4ptp-draft-03
experimental-ntp-over-ptp-draft-08

As of the baseline date, NTPv5 remains an Internet-Draft. Draft -09, dated 1 July 2026, retains only client and server operation and removes several legacy modes. It must therefore not be presented as a finished RFC or frozen into Mundilfari’s permanent stable API.

Roughtime draft -19 is also still a draft, although it has reached the RFC Editor queue. Mundilfari should implement the exact draft revision, retain its wire-version identity, and migrate only after an RFC is published.

3. Corrections to the original design

The original proposal is a strong beginning, but several architectural details need correction.

3.1 PTP and GPS do not share one epoch

PTP and GPS must never be merged into a single PtpGps epoch.

They have different:

Epoch semantics.
Time-scale semantics.
Leap-second behavior.
Wire encodings.
Rollover behavior.
Conversion requirements.

Every protocol timestamp must preserve its native epoch and scale until an explicit conversion is requested.

3.2 SystemTime cannot be the universal type

This is insufficient:

pub struct Timestamp {
    pub seconds: u64,
    pub fractional: u32,
    pub epoch: TimeEpoch,
}

It cannot safely express:

Dates before an epoch.
Leap seconds.
Negative offsets.
NTP eras.
GPS week rollovers.
PTP scaled nanoseconds.
White Rabbit precision.
UT1.
TAI.
Uncertain time intervals.
Clock quality.
Authentication state.
Source provenance.
Rounding introduced during conversion.
A monotonic timestamp with no civil-time correlation.

std::time::SystemTime should only be an optional platform conversion. It is not the canonical internal representation.

3.3 Daytime text cannot be silently trusted

RFC 867 deliberately does not prescribe one textual representation. A Daytime implementation may return arbitrary human-readable text. Mundilfari should return the original bytes and optionally report parse candidates.

It must not guess a date, silently convert it to SystemTime, and label the result authoritative.

3.4 SNTP is not an unrelated packet protocol

SNTP uses NTP packet formats and is operationally a simplified subset. Mundilfari should therefore have:

mundilfari-ntp-wire
mundilfari-sntp
mundilfari-ntp

mundilfari-ntp-wire owns shared packet formats. mundilfari-sntp implements constrained one-shot behavior. mundilfari-ntp implements full stateful synchronization.

RFC 5905 now needs to be read together with updates covering extension fields, MAC authentication, port randomization, registry changes, and interleaved modes.

3.5 Full NTP is not “query several servers and average them”

A production NTP implementation requires separate algorithms for:

Sample validation.
Clock filtering.
Root-distance calculation.
Candidate intersection.
Falseticker rejection.
Clustering.
System-peer selection.
Combining.
Loop avoidance.
Poll control.
Reachability.
Frequency estimation.
PLL/FLL discipline.
Panic thresholds.
Holdover.

Khronos should also be available as an independent security watchdog against time-shifting attacks. RFC 9523 explicitly defines this role.

3.6 Hardware PTP does not completely bypass the operating system

PTP may use:

Raw Ethernet.
UDP over IPv4.
UDP over IPv6.
Software socket timestamps.
Hardware receive timestamps.
Hardware transmit timestamps.
Linux PHC devices.
NIC driver ioctls.
Transparent-clock correction fields.

The Linux kernel and NIC driver remain essential parts of the timestamp path.

3.7 White Rabbit is not only a PTP TLV parser

White Rabbit requires support for:

A compatible PTP high-accuracy profile.
Frequency transfer.
Physical-layer synchronization.
Hardware clock control.
Link-delay calibration.
Phase tracking.
Fixed-delay compensation.
Suitable NIC, FPGA, or switch hardware.

A software-only implementation can inspect and generate messages, but cannot promise White Rabbit accuracy without compatible hardware.

4. Protocol universe

The original list omitted a significant part of the time ecosystem.

The following is the required starting inventory. PROTOCOLS.md will remain the authoritative machine-audited ledger.

4.1 Internet time protocols
mundilfari-daytime             RFC 867 Daytime
mundilfari-time                RFC 868 TIME
mundilfari-icmp-time           ICMP Timestamp Request and Reply
mundilfari-dcnet-clock         Historic DCNET Internet Clock Service
mundilfari-nist-acts           NIST Automated Computer Time Service
mundilfari-bsd-timed           BSD timed Time Synchronization Protocol
mundilfari-dce-dts             DCE Distributed Time Service
mundilfari-ms-sntp             Microsoft SNTP extensions
mundilfari-xmpp-time           XMPP Entity Time

Legacy protocols are disabled in secure default configurations. Supporting a protocol does not mean Mundilfari considers it safe for clock discipline.

4.2 NTP family
mundilfari-ntp-wire            Shared NTP packet and extension-field codecs
mundilfari-ntp-legacy          NTPv0, NTPv1, NTPv2 and NTPv3 compatibility
mundilfari-sntp                Historical and current SNTP behavior
mundilfari-ntp                 Full NTPv4 engine
mundilfari-ntp-control         Mode 6 control protocol
mundilfari-ntp-autokey         Autokey inspection and legacy compatibility
mundilfari-ntp-khronos         RFC 9523 secure selection watchdog
mundilfari-nts                 Network Time Security
mundilfari-ntpv5               Version-pinned NTPv5 draft implementation
mundilfari-ntp-over-ptp        Version-pinned IETF draft
mundilfari-nts4ptp             Version-pinned NTS-for-PTP draft
mundilfari-ntp-discovery       DHCP, configured pools and future discovery
mundilfari-ntp-management      MIB, YANG and management mappings

NTS uses TLS and authenticated encryption to protect NTP client-server operation.

NTS for PTP remains an active draft and must stay behind an experimental API until finalized.

4.3 Secure and evidence-producing time
mundilfari-roughtime
mundilfari-rfc3161
mundilfari-rfc5816
mundilfari-ers
mundilfari-xmlers
mundilfari-timestamped-data
mundilfari-cose-timestamp
mundilfari-etsi-timestamp
mundilfari-x995
mundilfari-authenticode-time
mundilfari-opentimestamps

These must distinguish two separate concepts:

Obtaining the current time.
Obtaining cryptographic evidence that data existed or was processed near a stated time.

An RFC 3161 token is evidence from a Time-Stamp Authority. It is not a drop-in replacement for a continuously synchronized local clock.

4.4 Precision time and frequency transfer
mundilfari-ptp-wire
mundilfari-ptp-v1
mundilfari-ptp
mundilfari-gptp
mundilfari-ptp-enterprise
mundilfari-ptp-telecom
mundilfari-ptp-power
mundilfari-ptp-media
mundilfari-ptp-fronthaul
mundilfari-white-rabbit
mundilfari-synce

The stable baseline must include:

IEEE 1588-2002 compatibility.
IEEE 1588-2008 compatibility.
IEEE 1588-2019.
IEEE 802.1AS-2011 where legacy interoperability is required.
IEEE 802.1AS-2020.
IEEE 1588 default profiles.
IETF Enterprise Profile.
ITU-T G.8265.1.
ITU-T G.8275.1.
ITU-T G.8275.2.
IEEE C37.238.
IEC/IEEE 61850-9-3.
SMPTE ST 2059-2.
AES67 timing profile.
IEEE 802.1CM-related fronthaul timing.
White Rabbit/high-accuracy operation.
Synchronous Ethernet messaging and quality levels.

IEEE currently identifies IEEE 1588-2019 as the precision clock synchronization standard, while IEEE 802.1AS-2020 defines generalized precision timing for bridged local-area networks.

The IETF Enterprise Profile is now RFC 9760 and targets IEEE 1588-2019 operation over IPv4 and IPv6 enterprise networks.

4.5 GNSS and satellite navigation time
mundilfari-nmea0183
mundilfari-nmea2000
mundilfari-gps
mundilfari-galileo
mundilfari-galileo-osnma
mundilfari-beidou
mundilfari-glonass
mundilfari-qzss
mundilfari-navic
mundilfari-sbas
mundilfari-rtcm
mundilfari-rinex
mundilfari-cggtts
mundilfari-twstft
mundilfari-gpsd

Separate vendor crates may include:

mundilfari-ubx
mundilfari-tsip
mundilfari-sirf
mundilfari-novatel
mundilfari-garmin

These are only implemented from vendor-published specifications.

GNSS support must include more than NMEA text. A complete receiver stack needs:

Raw navigation message decoding.
Parity and CRC validation.
Week and era resolution.
Health indicators.
UTC correction parameters.
Leap-second announcements.
Time-system correction parameters.
Signal identity.
Receiver time pulse information.
Uncertainty.
Spoofing and inconsistency indicators.
Correlation with PPS capture.
4.6 Pulse, serial, radio, and physical timecodes
mundilfari-pps
mundilfari-frequency-reference
mundilfari-irig
mundilfari-ieee1344
mundilfari-wwvb
mundilfari-wwv
mundilfari-chu
mundilfari-dcf77
mundilfari-msf
mundilfari-jjy
mundilfari-bpc
mundilfari-als162
mundilfari-rwm
mundilfari-bpm
mundilfari-eloran

IRIG implementation must be generated from the exact supported RCC revision and must cover every code and control-function layout defined by that revision—not merely a hardcoded IRIG-B example.

Radio implementations should separate:

Signal acquisition
Carrier or edge detection
Symbol classification
Frame synchronization
Parity validation
Civil-time decoding
Quality and announcement decoding
Time-source observation

NIST publicly documents WWVB and WWV/WWVH time codes, and other national laboratories publish specifications for CHU, MSF, JJY and DCF77.

4.7 Broadcast and media timing
mundilfari-smpte-timecode
mundilfari-midi-timecode
mundilfari-aes-time
mundilfari-rds-time
mundilfari-dvb-time
mundilfari-atsc-time
mundilfari-isdb-time
mundilfari-rtp-time
mundilfari-mpeg-time
mundilfari-dash-time
mundilfari-hls-time
mundilfari-scte-time

This family must distinguish:

Wall-clock time.
Media clock ticks.
Presentation timestamps.
Decode timestamps.
Program clock references.
Frame numbers.
Drop-frame numbering.
Capture-time correlation.
Clock source identity.

An RTP timestamp by itself is not a UTC timestamp. It becomes meaningful as wall time only through an explicit clock correlation, such as an RTCP sender report or another clock-source mapping.

4.8 Space systems
mundilfari-ccsds-time
mundilfari-spacewire-time
mundilfari-spacefibre-time
mundilfari-ecss-time

Required CCSDS support includes the time-code families defined by the selected normative revision, including:

Unsegmented codes.
Day-segmented codes.
Calendar-segmented codes.
ASCII representations.
Agency-defined epochs.
P-field handling.
Fine-time extensions.
Mission epoch registries.

CCSDS lists Time Code Formats as a current Blue Book in its official publication catalogue.

4.9 Industrial, energy, and building automation
mundilfari-bacnet-time
mundilfari-dnp3-time
mundilfari-iec60870-time
mundilfari-iec61850-time
mundilfari-canopen-time
mundilfari-j1939-time
mundilfari-ethercat-time
mundilfari-profinet-time
mundilfari-cip-sync
mundilfari-sercos-time
mundilfari-powerlink-time
mundilfari-knx-time
mundilfari-opcua-time

DNP3 explicitly includes time synchronization and time-stamped events. CIP Sync builds on IEEE 1588. EtherCAT has distributed clocks, while PROFINET uses synchronized mechanisms including gPTP for time-of-day synchronization.

Each crate must implement only the relevant time services. Mundilfari is not intended to become a complete DNP3, BACnet, or OPC UA stack.

For example, mundilfari-dnp3-time contains:

Time-related object codecs.
Delay measurement.
Time synchronization exchanges.
Event timestamp types.
Validation and state machines.

The application supplies or implements the surrounding DNP3 transport.

4.10 Automotive and deterministic networks
mundilfari-autosar-time
mundilfari-autosar-eth-time
mundilfari-autosar-can-time
mundilfari-autosar-flexray-time
mundilfari-flexray-time
mundilfari-ttethernet-time
mundilfari-tsn-time
mundilfari-oran-time

AUTOSAR publishes time-synchronization specifications for Ethernet, CAN, and FlexRay, while SAE AS6802 defines a fault-tolerant synchronization strategy for Time-Triggered Ethernet.

4.11 Wireless, IoT, and cellular time
mundilfari-bluetooth-time
mundilfari-bluetooth-mesh-time
mundilfari-zigbee-time
mundilfari-matter-time
mundilfari-lorawan-time
mundilfari-wifi-time
mundilfari-tsch-time
mundilfari-6tisch-time
mundilfari-wirelesshart-time
mundilfari-isa100-time
mundilfari-thread-time
mundilfari-nitz
mundilfari-5g-time

Bluetooth alone defines multiple relevant services and profiles, including Current Time, Reference Time Update, Device Time, Time Profile, and Elapsed Time.

LoRaWAN includes DeviceTimeReq and DeviceTimeAns for synchronizing an end device to network-provided GPS time.

Wi-Fi TSF and TSCH synchronization are not necessarily UTC distribution. The type system must classify them as local or network clock synchronization unless an explicit civil-time correlation is available.

4.12 Time representation, zone, and discovery standards
mundilfari-rfc3339
mundilfari-ixdtf
mundilfari-iso8601
mundilfari-http-date
mundilfari-asn1-time
mundilfari-tzif
mundilfari-tzdist
mundilfari-posix-tz
mundilfari-ical-timezone

These are not all clock synchronization protocols, but they are required to make the umbrella crate useful in applications, servers, websites, certificates, logs, and operating systems.

Mundilfari should support RFC 3339, IXDTF, TZif, and TZDIST as distinct formats and protocols, rather than assuming one generic “ISO date string.”

5. Workspace architecture
mundilfari-workspace/
├── Cargo.toml
├── PROTOCOLS.md
├── STANDARDS.md
├── SECURITY.md
├── UNSAFE.md
├── COMPATIBILITY.md
├── RELEASES.md
├── standards/
│   ├── registry.mf
│   ├── errata.mf
│   ├── licences.mf
│   └── hashes.mf
├── crates/
│   ├── foundation/
│   │   ├── mundilfari-core/
│   │   ├── mundilfari-calendar/
│   │   ├── mundilfari-timescale/
│   │   ├── mundilfari-leap/
│   │   ├── mundilfari-zone/
│   │   ├── mundilfari-uncertainty/
│   │   ├── mundilfari-quality/
│   │   ├── mundilfari-wire/
│   │   ├── mundilfari-buffer/
│   │   ├── mundilfari-state/
│   │   ├── mundilfari-clock/
│   │   ├── mundilfari-servo/
│   │   ├── mundilfari-consensus/
│   │   ├── mundilfari-policy/
│   │   └── mundilfari-registry/
│   ├── security/
│   │   ├── mundilfari-crypto/
│   │   ├── mundilfari-asn1/
│   │   ├── mundilfari-x509/
│   │   ├── mundilfari-tls/
│   │   ├── mundilfari-secrets/
│   │   └── mundilfari-trust/
│   ├── platform/
│   │   ├── mundilfari-io/
│   │   ├── mundilfari-sys/
│   │   ├── mundilfari-linux/
│   │   ├── mundilfari-windows/
│   │   ├── mundilfari-bsd/
│   │   ├── mundilfari-macos/
│   │   ├── mundilfari-embedded/
│   │   ├── mundilfari-reactor/
│   │   ├── mundilfari-hwtstamp/
│   │   ├── mundilfari-phc/
│   │   ├── mundilfari-pps/
│   │   └── mundilfari-resolver/
│   ├── internet/
│   │   ├── mundilfari-daytime/
│   │   ├── mundilfari-time/
│   │   ├── mundilfari-icmp-time/
│   │   ├── mundilfari-dcnet-clock/
│   │   ├── mundilfari-ntp-wire/
│   │   ├── mundilfari-sntp/
│   │   ├── mundilfari-ntp/
│   │   ├── mundilfari-ntp-control/
│   │   ├── mundilfari-ntp-autokey/
│   │   ├── mundilfari-ntp-khronos/
│   │   ├── mundilfari-nts/
│   │   ├── mundilfari-ntpv5/
│   │   ├── mundilfari-roughtime/
│   │   ├── mundilfari-ntp-over-ptp/
│   │   └── mundilfari-nts4ptp/
│   ├── precision/
│   │   ├── mundilfari-ptp-wire/
│   │   ├── mundilfari-ptp-v1/
│   │   ├── mundilfari-ptp/
│   │   ├── mundilfari-gptp/
│   │   ├── mundilfari-ptp-enterprise/
│   │   ├── mundilfari-ptp-telecom/
│   │   ├── mundilfari-ptp-power/
│   │   ├── mundilfari-ptp-media/
│   │   ├── mundilfari-white-rabbit/
│   │   └── mundilfari-synce/
│   ├── gnss/
│   ├── radio/
│   ├── broadcast/
│   ├── space/
│   ├── industrial/
│   ├── automotive/
│   ├── wireless/
│   ├── timestamping/
│   └── formats/
├── applications/
│   ├── mundilfari/
│   ├── mundilfari-cli/
│   ├── mundilfarid/
│   ├── mundilfari-privileged/
│   ├── mundilfari-c/
│   └── mundilfari-wasm/
└── testing/
    ├── mundilfari-testkit/
    ├── mundilfari-simulator/
    ├── mundilfari-fuzzer/
    ├── mundilfari-conformance/
    ├── mundilfari-packet-lab/
    └── mundilfari-hardware-lab/
6. Dependency architecture

The workspace must have a strict one-directional dependency graph.

Layer 0: integer, buffer, wire and core time primitives
       ↓
Layer 1: crypto, calendar, scale, uncertainty and clock abstractions
       ↓
Layer 2: protocol codecs and state machines
       ↓
Layer 3: transport, platform, hardware and operating-system adapters
       ↓
Layer 4: source selection, consensus, servo and orchestration
       ↓
Layer 5: umbrella crate, CLI, daemon, servers and foreign interfaces

Rules:

Protocol crates may not depend on the umbrella crate.
Core crates may not depend on protocol crates.
Wire parsers may not depend on operating-system code.
Platform crates may not contain protocol policy.
Clock discipline may not be embedded inside packet parsing.
Crypto may not depend on NTS or TLS.
TLS may depend on crypto and X.509, but not on NTS.
NTS may depend on TLS and NTP wire formats.
Profiles may depend on their base protocol, never the reverse.
Experimental draft crates may not leak draft-only types into stable foundation crates.

A workspace linter must reject dependency cycles and out-of-layer dependencies.

7. Zero-dependency policy

“No other crates” should be interpreted literally.

Allowed dependencies:

core
alloc, when explicitly enabled
std, when explicitly enabled
other Mundilfari workspace crates
operating-system system calls
operating-system kernel interfaces
hardware registers supplied by the application

Forbidden:

libc
tokio
async-std
smol
mio
socket2
serde
chrono
time
regex
rustls
ring
webpki
openssl
rand
getrandom
subtle
zeroize
byteorder
nom
bitflags
heapless
embedded-hal
windows-sys
bindgen
cc
proc-macro parsing crates
third-party development dependencies

This restriction applies to:

Normal dependencies.
Development dependencies.
Build dependencies.
Target-specific dependencies.
Optional dependencies.
Procedural macros.
Generated code requiring third-party build tools.

External verification programs may be run in CI, but they do not become Cargo dependencies and do not ship in the crate.

7.1 Dependency guard

Every build runs a workspace-owned checker that validates:

Every package dependency resolves inside the workspace.
No registry dependency appears.
No Git dependency appears.
No unapproved system library is linked.
No build script invokes an external compiler.
Published crate manifests preserve the same rule.

The repository should additionally build with Cargo’s network access disabled.

8. no_std capability model

Every crate documents one of four capability levels.

Level A: no_std, no allocation

Suitable for:

Packet parsing.
Packet generation.
Embedded state machines.
PPS handling.
IRIG decoding.
Fixed-size NTP clients.
PTP port state machines.
Time arithmetic.
Level B: no_std + alloc

Suitable for:

Dynamic source lists.
Dynamic certificate chains.
Variable-length audit records.
User-friendly owned strings.
Complex configuration.
Level C: std

Suitable for:

TCP and UDP sockets.
DNS resolution.
Files.
threads.
operating-system clocks.
command-line applications.
Level D: privileged platform

Suitable for:

Raw sockets.
SO_TIMESTAMPING.
PHC devices.
PPS devices.
clock_adjtime.
system-clock discipline.
NIC timestamp configuration.

Protocol crates use this pattern:

#![cfg_attr(not(feature = "std"), no_std)]

#[cfg(feature = "alloc")]
extern crate alloc;

Default features for protocol crates should be empty:

[features]
default = []
alloc = []
std = ["alloc"]
client = []
server = []
historical = []
experimental = []

The umbrella crate may default to a practical std configuration, but insecure historical protocols must not be enabled by default.

9. Core time model
9.1 Continuous internal instant

The preferred canonical instant is a continuous atomic timeline.

pub struct AtomicInstant {
    seconds: i128,
    attoseconds: u64,
}

Invariant:

attoseconds < 1_000_000_000_000_000_000

The internal origin is explicitly documented and never inferred from the type.

All arithmetic uses checked operations.

impl AtomicInstant {
    pub fn checked_add(self, delta: Duration) -> Option<Self>;
    pub fn checked_sub(self, delta: Duration) -> Option<Self>;
    pub fn duration_since(self, earlier: Self) -> Option<Duration>;
}
9.2 Exact protocol representation

Normalized time must not destroy original wire precision.

pub struct ProtocolTimestamp<R> {
    raw: R,
    normalized: AtomicInstant,
    quantization: Duration,
    rounding: RoundingDirection,
}

For example, an NTP fraction is retained as its original binary fraction. Conversion to attoseconds uses wide-integer arithmetic and reports the resulting quantization interval.

9.3 Wide intermediate arithmetic

Mundilfari requires internal U256 and I256 types for:

Fraction conversion.
Multiplication before division.
Fixed-point servo calculations.
Certificate arithmetic.
RSA.
Large date ranges.
Overflow-safe interval calculations.

These types belong to an internal arithmetic module and must not expose unchecked operations.

9.4 Time scales
pub enum TimeScale {
    Tai,
    Utc,
    Ut1,
    Gps,
    Galileo,
    Beidou,
    Glonass,
    Ptp,
    Ntp,
    Posix,
    TerrestrialTime,
    Tcg,
    Tcb,
    Tdb,
    Custom(TimeScaleId),
}

Scale conversion requires explicit data:

pub struct ScaleContext<'a> {
    leap_seconds: &'a LeapSecondTable,
    earth_orientation: Option<&'a EarthOrientationTable>,
    gnss_offsets: &'a GnssOffsetTable,
}

No conversion silently invents missing UT1 or leap-second information.

9.5 UTC and leap seconds

UTC must be capable of representing second 60:

pub struct UtcDateTime {
    pub date: GregorianDate,
    pub hour: u8,
    pub minute: u8,
    pub second: UtcSecond,
    pub attosecond: u64,
}

pub enum UtcSecond {
    Regular(u8),
    PositiveLeap,
}

Negative leap seconds must be structurally supported even though none has occurred yet.

Leap data is:

Versioned.
Hashable.
Replaceable.
Signed when distributed.
Associated with provenance.
Never silently downloaded by core code.
9.6 POSIX time is not UTC

POSIX timestamps receive their own type:

pub struct PosixInstant {
    seconds: i128,
    nanoseconds: u32,
}

Conversion between POSIX and UTC requires an explicit leap policy:

pub enum PosixLeapPolicy {
    RejectAmbiguous,
    RepeatPreviousSecond,
    Clamp,
    Smear(SmearProfile),
}

A smear is never reported as true UTC.

9.7 Epoch and era handling
pub struct EraContext {
    pub lower_bound: AtomicInstant,
    pub upper_bound: AtomicInstant,
}

pub trait EraResolver<R> {
    fn resolve(
        &self,
        raw: R,
        context: EraContext,
    ) -> Result<AtomicInstant, EraError>;
}

Required rollover handling includes:

RFC 868 32-bit rollover.
NTP eras.
GPS week rollover.
Truncated GNSS week fields.
Short broadcast counters.
Device uptime counter wrap.
PTP seconds-field limits.
User-defined mission epochs.

A conversion requiring context returns an error when context is absent. It must not choose the nearest era without informing the caller.

9.8 Uncertainty as a first-class value
pub struct TimeInterval {
    pub earliest: AtomicInstant,
    pub latest: AtomicInstant,
}

pub struct Uncertainty {
    pub negative: Duration,
    pub positive: Duration,
}

A network reading should usually be represented as an interval, not a magical exact nanosecond.

9.9 Time quality
pub struct TimeQuality {
    pub uncertainty: Uncertainty,
    pub resolution: Duration,
    pub precision: Duration,
    pub age: Duration,
    pub stability: StabilityEstimate,
    pub traceability: Traceability,
    pub leap_state: LeapState,
    pub holdover: HoldoverState,
}
9.10 Authentication and accuracy are separate
pub enum Authentication {
    None,
    SymmetricMac,
    ServerAuthenticated,
    MutuallyAuthenticated,
    SignedPhysicalSource,
    EvidenceChain,
}

pub enum SourceAccuracy {
    Unknown,
    Advertised(Uncertainty),
    Measured(Uncertainty),
    Verified(Uncertainty),
}

An authenticated server can be compromised or misconfigured.

An unauthenticated GNSS receiver can be accurate at one moment but spoofable.

The API must never collapse these properties into one trusted: bool.

9.11 Provenance
pub struct Provenance {
    pub source: SourceIdentity,
    pub protocol: ProtocolIdentity,
    pub authority: Option<AuthorityIdentity>,
    pub path: PathIdentity,
    pub raw_observation_hash: ObservationHash,
    pub received_at: MonotonicInstant,
}
9.12 Complete reading type
pub struct TimeReading {
    pub interval: TimeInterval,
    pub estimated: AtomicInstant,
    pub local_capture: MonotonicInstant,
    pub offset: SignedDuration,
    pub delay: Option<Duration>,
    pub quality: TimeQuality,
    pub authentication: Authentication,
    pub provenance: Provenance,
    pub warnings: WarningSet,
}
10. Monotonic and civil clocks

Mundilfari must model at least four different clock concepts.

Monotonic clock
Continuous atomic time
Civil UTC time
Local zoned time

A monotonic reading cannot be directly converted to UTC without a correlation:

pub struct ClockCorrelation {
    pub monotonic: MonotonicInstant,
    pub atomic: AtomicInstant,
    pub uncertainty: Uncertainty,
    pub rate: FrequencyRatio,
}

Applications can then obtain a fast trusted clock without performing a network request for every timestamp.

let reading = trusted_clock.read()?;
println!("{}", reading.utc(&leap_table)?);

This design is particularly important for:

Web servers.
Databases.
Certificate validation.
Logging.
Token expiry.
Distributed tracing.
Event ordering.
Long-running daemons.
11. Protocol-crate internal template

Every protocol crate should follow a common structure.

mundilfari-<protocol>/
├── Cargo.toml
├── README.md
├── SPECIFICATIONS.md
├── CONFORMANCE.md
├── SECURITY.md
├── ERRATA.md
├── TESTING.md
├── src/
│   ├── lib.rs
│   ├── constants.rs
│   ├── wire.rs
│   ├── message.rs
│   ├── decode.rs
│   ├── encode.rs
│   ├── validate.rs
│   ├── state.rs
│   ├── client.rs
│   ├── server.rs
│   ├── policy.rs
│   ├── error.rs
│   └── std_support.rs
└── tests/
    ├── official_vectors/
    ├── malformed/
    ├── interoperability/
    └── regressions/

Not every protocol needs every source file, but the architectural concepts remain consistent.

11.1 Parsing and validation are separate
let packet = PacketRef::parse(bytes)?;
let validated = packet.validate(&policy)?;

The parser answers:

Can these bytes be structurally decoded?

The validator answers:

Is this message valid, safe, expected, and acceptable under the current protocol state and policy?

This allows forensic tools to inspect malformed packets without treating them as valid protocol input.

11.2 Borrowed parsing
pub struct PacketRef<'a> {
    bytes: &'a [u8],
    header: Header,
    extensions: ExtensionIter<'a>,
}

Benefits:

No allocation.
No copy.
Original bytes preserved.
Unknown extensions remain inspectable.
Suitable for embedded and packet-analysis use.
11.3 Caller-owned encoding
let mut output = [0u8; 512];
let length = message.encode(&mut output)?;
transport.send(&output[..length])?;

No protocol encoder allocates unless the caller explicitly enables an owned API.

11.4 Strict default parser
pub enum DecodeMode {
    Strict,
    Compatible,
    Forensic,
}

Strict is the default.

Compatible permits explicitly documented interoperable deviations.

Forensic preserves malformed and reserved values with warnings, but those values cannot enter clock-discipline state.

11.5 Unknown-field preservation

Extension-based protocols must preserve unknown fields:

pub enum ExtensionRef<'a> {
    Known(KnownExtension<'a>),
    Unknown {
        type_id: u16,
        value: &'a [u8],
    },
}

This prevents a parser-update bottleneck and permits gateways to relay extensions they do not understand.

12. I/O abstraction

Protocol engines must not directly depend on sockets.

pub trait DatagramTransport {
    type Address;
    type Error;

    fn poll_send(
        &mut self,
        packet: &[u8],
        destination: &Self::Address,
        context: &mut PollContext<'_>,
    ) -> Poll<Result<SendMetadata, Self::Error>>;

    fn poll_receive(
        &mut self,
        buffer: &mut [u8],
        context: &mut PollContext<'_>,
    ) -> Poll<Result<ReceivedDatagram<Self::Address>, Self::Error>>;
}

Equivalent traits are required for:

Stream transports.
Raw Ethernet.
ICMP.
Serial ports.
Edge capture.
Audio/sample streams.
CAN.
FlexRay adapters.
Bluetooth GATT.
Hardware register access.
Entropy sources.
Clocks.
PHC devices.

A protocol crate can therefore run with:

Linux sockets.
An embedded network stack.
A simulator.
A packet capture.
A test harness.
A user’s own executor.
A virtual network.
13. Async architecture without Tokio

Mundilfari must not depend on Tokio or another runtime.

It should provide three execution models.

13.1 Pure polling
match client.poll(&mut transport, &mut clock, &mut context)? {
    Poll::Pending => {}
    Poll::Ready(report) => use_report(report),
}

This is the canonical no_std API.

13.2 Rust Future adapters

The workspace may expose futures built entirely from core::future and the Mundilfari poll traits.

These futures can be driven by:

Mundilfari’s runtime.
A user-provided executor.
Tokio through adapter code written in the user’s application.
An embedded executor.

Mundilfari itself does not depend on that executor.

13.3 Own optional runtime

mundilfari-reactor implements:

epoll on Linux.
kqueue on BSD and macOS.
IOCP on Windows.
A timer queue.
Waker registration.
Socket readiness.
Cancellation.
Bounded task storage.

The runtime is optional and not used by protocol cores.

14. Linux platform layer

Linux is the reference full-feature platform.

14.1 Handwritten ABI

Because libc and bindgen are forbidden, Mundilfari must maintain its own audited ABI definitions for:

Socket structures.
sockaddr.
msghdr.
cmsghdr.
timespec.
timex.
ifreq.
hwtstamp_config.
PTP ioctl structures.
PPS structures.
Netlink structures.

Every definition must be validated against supported kernel UAPI headers in CI.

No wire or kernel structure should be decoded by transmuting a byte slice.

14.2 Required Linux capabilities
UDP and TCP sockets
Raw ICMP sockets
AF_PACKET raw Ethernet
SO_TIMESTAMP
SO_TIMESTAMPNS
SO_TIMESTAMPING
SCM_TIMESTAMPING
SIOCSHWTSTAMP
PTP_CLOCK_GETCAPS
PTP_SYS_OFFSET
PTP_SYS_OFFSET_EXTENDED
PTP_SYS_OFFSET_PRECISE
clock_adjtime
adjtimex
clock_settime
/dev/ptpN
/dev/ppsN
RTC ioctls
ethtool or netlink timestamp capability discovery
14.3 Ancillary-data parsing

Control-message parsing must:

Validate alignment.
Validate the complete cmsghdr.
Reject truncated control data.
Avoid integer overflow.
Handle multiple timestamp records.
Distinguish software, transformed hardware, and raw hardware timestamps.
Associate transmit timestamps with the correct outgoing packet.
Detect kernel drop counters where available.
14.4 PHC support
pub trait HardwareClock {
    fn capabilities(&self) -> Result<ClockCapabilities, ClockError>;
    fn read(&self) -> Result<ClockReading, ClockError>;
    fn cross_timestamp(
        &self,
        system: &dyn Clock,
    ) -> Result<CrossTimestamp, ClockError>;
    fn adjust_frequency(&mut self, adjustment: FrequencyAdjustment)
        -> Result<(), ClockError>;
    fn adjust_phase(&mut self, adjustment: PhaseAdjustment)
        -> Result<(), ClockError>;
}
14.5 Privilege separation

mundilfarid must not run its entire synchronization engine as root.

Recommended process design:

Unprivileged source workers
            ↓
Unprivileged validation and consensus engine
            ↓
Bounded authenticated local IPC
            ↓
Minimal clock-discipline helper

A separate raw-socket helper may be used for ICMP or Layer-2 PTP.

The privileged helper accepts only constrained commands such as:

pub enum PrivilegedRequest {
    Slew {
        parts_per_billion: i64,
        maximum_duration: Duration,
    },
    StepForward {
        amount: Duration,
    },
    SetLeapState {
        state: LeapState,
    },
    AdjustPhc {
        clock: ClockId,
        adjustment: ClockAdjustment,
    },
}

It does not accept arbitrary file paths, ioctl numbers, pointers, or raw syscalls.

15. Cryptographic architecture

Implementing NTS without external crates requires Mundilfari to implement its own cryptographic and TLS stack.

This is the highest-risk part of the project.

Zero dependencies reduce supply-chain exposure, but they transfer the entire cryptographic correctness and side-channel burden to Mundilfari.

15.1 Required primitives

mundilfari-crypto needs:

SHA-256
SHA-384
HMAC
HKDF
AES-128
AES-256
AES-CMAC
AES-SIV-CMAC
AES-GCM
ChaCha20
Poly1305
ChaCha20-Poly1305
X25519
Ed25519
P-256
P-384
ECDSA
RSA verification
RSA-PSS
PKCS#1 v1.5 certificate-signature verification
constant-time comparison
secure secret storage
platform entropy adapters

Only algorithms actually required by standards should be enabled in minimal builds.

15.2 Constant-time rules

Secret-dependent code must not:

Branch on secret values.
Index lookup tables using secret values.
Return early after a partial tag comparison.
Use variable-time division on secrets.
Expose secret-dependent error differences.
Leave secret data in reusable buffers.

Portable fallbacks should prefer constant-time bitsliced or arithmetic designs.

Hardware acceleration may use:

AES-NI.
SHA extensions.
ARM cryptographic extensions.

Hardware and portable implementations must pass identical test vectors.

15.3 Secret types
pub struct SecretBytes<const N: usize> {
    bytes: [u8; N],
}

Requirements:

No Debug output containing contents.
No accidental Clone.
Explicit controlled exposure.
Volatile clearing.
Compiler fence.
Stack and heap clearing where possible.
Constant-time equality.
No serialization API by default.
15.4 Entropy
pub trait EntropySource {
    type Error;

    fn fill(&mut self, output: &mut [u8]) -> Result<(), Self::Error>;
}

Platform sources:

Linux getrandom.
BSD/macOS getentropy or native equivalent.
Windows CNG random generation.
Embedded application-supplied hardware RNG.

There must be no automatic fallback to:

Time-based seeds.
Process identifiers.
Memory addresses.
Xorshift.
An unseeded deterministic generator.

Failure to obtain cryptographic entropy is a hard error.

16. TLS 1.3

mundilfari-tls exists primarily to support NTS, but must still implement TLS correctly.

Required scope:

TLS 1.3 record layer
Handshake transcript
HKDF key schedule
ClientHello and ServerHello
HelloRetryRequest
EncryptedExtensions
Certificate
CertificateVerify
Finished
NewSessionTicket
SNI
ALPN
supported_versions
signature_algorithms
supported_groups
key_share
record-size limits
session resumption
orderly shutdown
alert handling

NTS uses an ALPN identifier and TLS-based key establishment. The TLS implementation must not silently negotiate older TLS versions.

16.1 X.509

mundilfari-asn1 and mundilfari-x509 must provide:

Strict DER parser.
Bounded recursion.
Definite-length enforcement.
Integer minimality checks.
OID parsing.
Certificate chain construction.
Basic constraints.
Key usage.
Extended key usage.
Subject alternative names.
Name constraints.
Path-length constraints.
Algorithm constraints.
DNS service identity.
Validity intervals.
Trust anchors.
Revocation policy hooks.
Unknown critical-extension rejection.
16.2 Time-bootstrap paradox

Certificate validation requires reasonably correct time, while NTS may be the mechanism used to obtain correct time.

Mundilfari needs an explicit bootstrap state machine:

No trusted civil time
        ↓
Pinned Roughtime keys or pinned NTS server key
        ↓
Authenticated rough time interval
        ↓
Certificate validity interval can be evaluated
        ↓
Normal NTS exchange
        ↓
Precise authenticated synchronization

Alternative policy:

User-provided initial time interval.
Provisioned device manufacturing time.
Hardware secure clock.
Previously persisted trusted interval plus elapsed monotonic time.
Explicit SPKI pin.

Mundilfari must never solve the paradox by silently disabling certificate validity checks.

17. NTP architecture
17.1 Observation timestamps

An exchange records:

pub struct FourTimestampExchange {
    pub client_send: ClockSample,
    pub server_receive: NtpTimestamp,
    pub server_send: NtpTimestamp,
    pub client_receive: ClockSample,
}

Offset:

((T2 - T1) + (T3 - T4)) / 2

Delay:

(T4 - T1) - (T3 - T2)

All calculations use checked fixed-point arithmetic.

17.2 Packet validation

Before an observation enters the filter:

Source address and port policy match.
Mode is expected.
Version is allowed.
Origin timestamp matches.
Packet is not truncated.
Stratum is valid.
Timestamps are ordered where required.
Root delay and dispersion are bounded.
Reference time is plausible.
Extension fields are structurally valid.
Authentication succeeds when required.
Replay checks succeed.
KoD handling is applied.
Era resolution is unambiguous.
Rate limits are respected.
17.3 Source state
pub struct NtpAssociation<const SAMPLES: usize> {
    reach: u8,
    poll: PollExponent,
    filter: ClockFilter<SAMPLES>,
    last_origin: NtpTimestamp,
    last_receive: MonotonicInstant,
    root_distance: Duration,
    jitter: Duration,
    state: AssociationState,
}
17.4 Selection stages
Admission
Sanity and authentication
Clock filter
Interval construction
Intersection
Falseticker rejection
Clustering
System-peer selection
Combining
Khronos watchdog
Servo input

Source diversity should consider:

Operator.
Autonomous system.
IP prefix.
Geographic path.
Protocol.
Physical reference source.
Shared upstream.
Authentication authority.

Four hostnames operated by one organization are not automatically four independent sources.

17.5 NTP server protections
Response never exceeds amplification policy.
Rate limits are per source and global.
KoD responses are controlled.
Mode 6 is disabled remotely by default.
No mode 7 private protocol.
Symmetric and broadcast modes require explicit configuration.
Unauthenticated control cannot alter state.
Source-port randomization is used where applicable.
Request fields are validated before expensive work.
NTS cookie processing is bounded.
Server cookies rotate keys safely.
No response is sent for certain malformed or suspicious requests.

RFC 7384 and RFC 8633 should be treated as mandatory security-design inputs, not optional reading.

18. NTS architecture

NTS has two distinct state machines.

18.1 NTS Key Establishment
TCP connection
TLS 1.3
ALPN verification
NTS record exchange
AEAD negotiation
NTP endpoint negotiation
Exporter-based key derivation
Cookie collection
Clean shutdown
18.2 Protected NTP exchange
Unique Identifier extension
NTS Cookie extension
Cookie Placeholder extensions
Authenticator and Encrypted Extension
AEAD verification
Replay validation
Cookie replenishment
18.3 Cookie jar

A bounded no_std client can use:

pub struct CookieJar<const COUNT: usize, const MAX_COOKIE: usize> {
    cookies: [CookieSlot<MAX_COOKIE>; COUNT],
}

The jar tracks:

Server identity.
AEAD algorithm.
C2S and S2C keys.
Expiry policy.
Used-cookie state.
Key-establishment generation.
Endpoint.
Failure count.

A cookie must never be reused contrary to protocol requirements.

19. Roughtime architecture

Roughtime returns a signed time interval rather than pretending to provide an exact UTC point.

pub struct RoughTimeReading {
    pub interval: TimeInterval,
    pub radius: Duration,
    pub server_key: RoughtimePublicKey,
    pub nonce: Nonce,
    pub delegation: DelegationEvidence,
    pub signature: SignatureEvidence,
    pub merkle_path: MerklePath,
}

Required verification order:

Message structure
Tag uniqueness
Length bounds
Nonce linkage
Merkle path
Certificate/delegation validity
Delegated key validity interval
Response signature
Time-radius constraints
Server identity policy

Roughtime should feed the bootstrap and consensus layers. It should not directly step the operating-system clock.

20. PTP architecture
20.1 Message support
Sync
Delay_Req
Pdelay_Req
Pdelay_Resp
Follow_Up
Delay_Resp
Pdelay_Resp_Follow_Up
Announce
Signaling
Management
All required TLVs
Unknown TLV preservation
20.2 Clock roles
pub enum ClockRole {
    Ordinary,
    Boundary,
    EndToEndTransparent,
    PeerToPeerTransparent,
    ManagementOnly,
    Monitor,
}
20.3 Port state machine

The engine must implement all required state transitions, timers, qualification rules, announce receipt timeouts, and role changes.

pub struct PtpPort<P: PtpProfile, T: PtpTransport> {
    profile: P,
    transport: T,
    state: PortState,
    foreign_masters: ForeignMasterDataset,
    timers: PtpTimers,
}
20.4 Profile abstraction
pub trait PtpProfile {
    fn profile_id(&self) -> ProfileId;
    fn allowed_transport(&self, transport: TransportKind) -> bool;
    fn allowed_delay_mechanism(&self, delay: DelayMechanism) -> bool;
    fn announce_interval(&self) -> IntervalRange;
    fn sync_interval(&self) -> IntervalRange;
    fn select_master(
        &self,
        candidates: &[ForeignMaster],
    ) -> SelectionResult;
    fn validate_tlv(&self, tlv: TlvRef<'_>) -> ValidationResult;
}

Profiles are separate crates because they can change:

BMCA behavior.
Message intervals.
Domain values.
Transport.
Delay mechanism.
TLV requirements.
Clock-class requirements.
Traceability rules.
Security expectations.
20.5 Delay attacks

Authentication alone does not prevent an attacker from delaying packets.

PTP defenses need:

Redundant paths.
Path asymmetry monitoring.
Delay-history limits.
Neighbor-rate ratio checks.
Physical topology policy.
Multiple grandmaster comparison.
GNSS or local reference comparison.
Sudden correction-field change detection.
Boundary and transparent-clock identity tracking.
20.6 Accuracy claims

Mundilfari must never claim nanosecond synchronization merely because a PTP packet was decoded.

Accuracy depends on:

Timestamp point.
NIC.
PHY.
Driver.
Switch behavior.
Cable asymmetry.
Oscillator.
Servo.
Profile.
Calibration.
Network load.
Hardware architecture.
21. GNSS and signal-fusion architecture

GNSS decoding has three layers:

Receiver protocol
Navigation message
Clock observation

A receiver saying “UTC 12:00” is not enough. Mundilfari must retain:

Constellation.
Signal.
Satellite.
Receiver identity.
Fix status.
Time-valid status.
Leap validity.
UTC model age.
Navigation-message issue.
Receiver clock bias.
PPS relation.
Estimated error.
Jamming indicators.
Spoofing indicators.

Fusion should compare:

GNSS civil message
PPS edge
Local oscillator
NTP/NTS
PTP
National radio
Roughtime interval
Previously trusted holdover

A GNSS source can be authenticated at the navigation layer, as with Galileo OSNMA, while still being subject to RF relay or meaconing. Authentication status and path-delay risk remain separate.

22. Clock discipline

Clock discipline must be reusable independently of NTP.

pub trait ClockServo {
    fn reset(&mut self, state: ServoReset);
    fn observe(&mut self, sample: ServoSample) -> ServoDecision;
}

Supported engines before 1.0:

Step-only test servo.
Bounded slew servo.
PLL.
FLL.
Hybrid PLL/FLL.
PTP-oriented phase/frequency servo.
Fixed-point Kalman-style estimator.
Holdover oscillator model.
Temperature-compensated model through user observations.
22.1 Clock targets
pub enum DisciplineTarget {
    VirtualApplicationClock,
    SystemRealtimeClock,
    HardwareClock(ClockId),
    RealtimeClockDevice(RtcId),
    PtpDomain(DomainId),
}
22.2 Safe default policy
Never step automatically after initial synchronization.
Never step backward by default.
Large initial correction requires explicit policy.
Large unexpected correction moves the engine to Faulted.
Slew rate is bounded.
Frequency correction is bounded.
Leap behavior is explicit.
Loss of all sources enters holdover.
Uncertainty grows during holdover.
Recovery from holdover is gradual unless policy authorizes a step.
23. Source consensus

A secure clock should not rely blindly on one protocol.

pub struct ConsensusPolicy {
    pub minimum_sources: usize,
    pub minimum_authenticated_sources: usize,
    pub maximum_interval_width: Duration,
    pub maximum_source_offset: Duration,
    pub diversity: DiversityPolicy,
}

Consensus operates on intervals:

Normalize observations to one continuous scale
Expand for source and network uncertainty
Reject policy failures
Group correlated sources
Find supported interval intersection
Apply authentication and diversity weights
Detect split-brain time
Select estimate inside accepted interval
Report complete evidence

Possible result:

pub enum ConsensusResult {
    Synchronized(TimeReading),
    Rough(TimeInterval),
    SplitBrain(SplitBrainReport),
    InsufficientSources(SourceFailureReport),
    Unsafe(SourceFailureReport),
}
24. User-facing APIs

Mundilfari needs both very easy APIs and deep expert APIs.

24.1 Read the local clock
let now = mundilfari::local_now()?;

This is explicitly the operating-system clock, not verified network time.

24.2 One authenticated query
use mundilfari::{NtsClient, ServerName};

let report = NtsClient::builder()
    .server(ServerName::parse("time.example.net")?)
    .system_trust_store()?
    .build()?
    .query_blocking()?;

println!("Offset: {}", report.offset());
println!("Uncertainty: {}", report.quality().uncertainty);
24.3 Secure multi-source clock
use mundilfari::{
    TrustedClock,
    policy::SecurityPolicy,
    source::{NtsSource, RoughtimeSource},
};

let clock = TrustedClock::builder()
    .policy(SecurityPolicy::strict())
    .source(NtsSource::new("time-a.example.net")?)
    .source(NtsSource::new("time-b.example.net")?)
    .source(RoughtimeSource::pinned(
        "roughtime.example.net",
        server_key,
    )?)
    .build()?;

let initial = clock.synchronize_blocking()?;
let current = clock.read()?;
24.4 Fixed-storage no_std client
let mut packet_buffer = [0u8; 512];
let mut response_buffer = [0u8; 512];

let mut client = mundilfari_sntp::Client::new(
    SntpConfig::strict(),
    &mut packet_buffer,
    &mut response_buffer,
);

let action = client.begin(local_clock.read()?);

transport.execute(action)?;

let report = client.finish(
    transport.received_bytes(),
    local_clock.read()?,
)?;
24.5 Linux daemon
let daemon = mundilfari::daemon::Builder::new()
    .source(NtsSource::new("time-a.example.net")?)
    .source(NtsSource::new("time-b.example.net")?)
    .source(PtpSource::domain(0))
    .target(SystemRealtimeClock)
    .servo(HybridServo::conservative())
    .step_policy(StepPolicy::startup_only(
        Duration::from_seconds(5),
    ))
    .holdover(HoldoverPolicy::enabled())
    .privilege_separation(true)
    .build()?;

daemon.run()?;
24.6 Protocol inspection
let packet = mundilfari_ntp_wire::PacketRef::parse(bytes)?;

println!("Version: {}", packet.version());
println!("Mode: {:?}", packet.mode());

for field in packet.extension_fields() {
    println!("{field:?}");
}
24.7 NMEA stream
let mut decoder = mundilfari_nmea0183::Decoder::<256>::new();

for byte in serial_bytes {
    if let Some(sentence) = decoder.push(byte)? {
        match sentence {
            Sentence::Zda(zda) => consume_time(zda.time_reading()?),
            Sentence::Rmc(rmc) => consume_navigation(rmc),
            _ => {}
        }
    }
}
24.8 IRIG edge decoder
let mut decoder = mundilfari_irig::Decoder::new(
    IrigProfile::B,
    IrigInput::DcLevelShift,
);

for edge in captured_edges {
    if let Some(frame) = decoder.observe(edge)? {
        let reading = frame.to_time_reading(&year_context)?;
        consume(reading);
    }
}
24.9 PTP clock
let mut engine = PtpEngine::<Gptp2020, 4, 16>::new(
    Gptp2020::default(),
    hardware_clock,
    ethernet_transport,
    storage,
)?;

loop {
    engine.poll(&mut context)?;
}
24.10 Trusted timestamp request
let token = Rfc3161Client::builder()
    .authority("tsa.example.net")?
    .digest_algorithm(DigestAlgorithm::Sha256)
    .require_nonce(true)
    .build()?
    .timestamp(document_digest)?;

token.verify(&trust_policy)?;
25. Website and WASM support

A browser cannot normally open:

UDP port 123.
Raw ICMP.
Raw Ethernet PTP.
/dev/ptpN.
Serial devices without browser-mediated APIs.
Kernel clock-control interfaces.

Therefore mundilfari-wasm should provide:

Core time types.
Date and scale conversions.
RFC 3339 and IXDTF.
TZif parsing.
NTP/PTP/Roughtime packet parsing.
Roughtime signature verification.
RFC 3161 token verification.
Time-reading and uncertainty display.
User-provided JavaScript transport hooks.

Backend websites can use the complete std client or connect to mundilfarid.

The crate must not invent a proprietary web time protocol merely to make browser examples appear simple.

26. Error architecture

Errors should remain structured in no_std.

pub enum Error {
    Decode(DecodeError),
    Validation(ValidationError),
    Authentication(AuthenticationError),
    Protocol(ProtocolError),
    Transport(TransportError),
    Clock(ClockError),
    Policy(PolicyError),
    Resource(ResourceError),
    Unsupported(UnsupportedError),
}

A decode error includes:

pub struct DecodeError {
    pub kind: DecodeErrorKind,
    pub offset: usize,
    pub field: Option<FieldId>,
}

No error should include:

Secret key bytes.
Cookies.
Passwords.
Complete certificates unless explicitly requested.
Full untrusted payloads.
Memory addresses.
27. Security policy
27.1 Security modes
pub enum SecurityPolicy {
    Strict,
    Balanced,
    Compatibility,
    Forensic,
}
Strict
Authenticated sources required.
No protocol downgrade.
No automatic Daytime, TIME, ICMP, SNTP, or unauthenticated NTP discipline.
Strong source diversity.
Bounded time changes.
Certificate verification required.
Draft protocols disabled unless explicitly enabled.
Historical modes disabled.
Balanced
Authenticated sources preferred.
Unauthenticated observations may be used for comparison.
They cannot independently authorize a large clock change.
Configured private PTP domains may be accepted under network policy.
Compatibility
Legacy protocols permitted.
Every insecure result is marked.
System-clock discipline still requires a separate explicit permission.
Forensic
Malformed and historical packets can be inspected.
No clock modification.
No value is automatically treated as trusted.
27.2 Threat model
Threat	Required controls
Off-path packet injection	Random ports, nonces, origin matching, unpredictable identifiers, authentication
Replay	Unique request state, replay windows, used-cookie tracking, monotonic state
Malicious time server	Source diversity, interval consensus, Khronos, maximum offset policy
Delay attack	Multiple paths, asymmetry detection, PTP monitoring, uncertainty growth
DNS poisoning	Authenticated protocol, pinned identities, resolver policy
Downgrade	Protocol pinning, no silent NTS-to-NTP fallback
Amplification	Small bounded replies, rate limits, request validation
Parser denial of service	Bounded lengths, bounded nesting, no untrusted allocation
CPU exhaustion	Work budgets, cookie-before-signature where standards permit, per-peer quotas
Memory exhaustion	Fixed capacities, explicit limits, no attacker-controlled vectors
Clock rollback	Monotonic guard, backward-step policy, application virtual clock
Compromised local user	Privilege separation, authenticated local IPC, permission checks
Compromised daemon worker	Minimal privileged helper and bounded commands
GNSS spoofing	Multi-source comparison, signal-health checks, authenticated navigation where available
Radio spoofing	Multiple receivers, propagation plausibility, other source comparison
PTP delay manipulation	Topology policy, redundant paths, correction monitoring
Faulty leap data	Signed and versioned tables, provenance, activation checks
Supply-chain compromise	Zero external Rust dependencies, reproducible builds, signed releases
Cryptographic side channel	Constant-time code, audits, hardware and portable tests
28. Parser hardening rules

All untrusted parsers must satisfy:

No panics for any byte sequence.
No unchecked slice indexing.
No integer arithmetic before bounds validation.
No recursive parsing without a depth limit.
No allocation based directly on untrusted length.
No unsafe in ordinary protocol parsing.
No transmute from network bytes.
No packed-structure field references.
No silent truncation.
No lossy UTF-8 conversion unless explicitly requested.
No canonicalization before signature verification when the protocol signs raw bytes.
Unknown critical fields cause validation failure.
Reserved values remain visible in forensic mode.
Errors identify the byte offset.

Every parser must be exhaustively tested for all inputs when the complete input space is small enough.

29. Unsafe-code policy

Allowed unsafe-code domains:

System-call and FFI boundaries
SIMD and CPU intrinsics
Volatile secret clearing
Ancillary control-message traversal
Memory-mapped hardware supplied by the application

Forbidden unsafe uses:

Routine packet parsing
Ordinary date arithmetic
Avoiding bounds checks for premature optimization
Casting wire packets to Rust structs
Constructing arbitrary references from network data
Global mutable state

Every unsafe block requires:

A SAFETY: explanation.
A linked invariant.
Unit tests.
Architecture-specific tests where applicable.
Inclusion in UNSAFE.md.
Review during every changed-release pentest.

The workspace should use:

#![deny(unsafe_op_in_unsafe_fn)]
30. Standards and conformance governance

Each protocol crate contains a clause map.

Example:

RFC 5905 §7.3       src/wire.rs::NtpHeader
RFC 5905 §8         src/state.rs::Association
RFC 7822 §3         src/extensions.rs
RFC 8573 §3         src/mac.rs
RFC 9109 §4         src/client.rs::PortPolicy
RFC 9769 §4         src/interleaved.rs
Verified Erratum X  tests/regression/...

Every specification record contains:

Title
Publisher
Identifier
Revision
Publication date
Status
Normative or informative
Official source
Local document hash, where legally held
Licence restrictions
Implemented clauses
Excluded clauses
Known errata
Conformance-test source
Last review date
30.1 Proprietary standards

IEEE, ISO, IEC, SMPTE, NMEA, ITU, AUTOSAR, and similar documents may have redistribution restrictions.

Mundilfari should not commit unauthorized copies.

The repository may contain:

Document identifier.
Revision.
SHA-256 hash.
Clause references.
Notes written independently.
Test vectors that may legally be redistributed.
Instructions for developers to provide their own licensed copy.

Normative wording must not be reconstructed from random websites or another implementation.

30.2 Compliance levels
pub enum ComplianceLevel {
    CodecComplete,
    ClientComplete,
    ServerComplete,
    StateMachineComplete,
    ProfileComplete,
    InteroperabilityTested,
    OfficialTestSuitePassed,
    ExternallyCertified,
}

Mundilfari must never use “certified” merely because internal tests pass.

31. Test architecture
31.1 Test categories

Every protocol crate requires:

Official positive vectors
Official negative vectors
Boundary values
Malformed lengths
Unknown fields
Reserved values
Round-trip tests
State-machine transition tests
Timer tests
Replay tests
Resource-limit tests
Rollover tests
Leap-second tests
Cross-endian tests
Interoperability tests
Fuzz regressions
31.2 Own property-test engine

Because no property-testing crate may be used, mundilfari-testkit supplies:

Deterministic PRNG for testing only.
Value generators.
Shrinking.
Invariant runner.
Seed recording.
Corpus replay.
Failure minimization.

The testing PRNG must never be exposed as cryptographic entropy.

31.3 Own mutational fuzzer

mundilfari-fuzzer provides:

Bit flips.
Byte insertion and deletion.
Length corruption.
Integer boundary mutation.
TLV reordering.
Duplicate-field generation.
Truncation.
Checksum corruption.
State-sequence mutation.
Timing-event mutation.

External fuzzers can additionally execute test binaries, but Mundilfari does not depend on their crates.

31.4 Network simulator

The simulator must model:

Delay.
Jitter.
Loss.
Duplication.
Reordering.
Fragmentation.
Asymmetric paths.
Clock drift.
Clock steps.
Oscillator noise.
Leap seconds.
Era rollover.
Malicious sources.
Delayed authenticated packets.
Byzantine source groups.
Server restarts.
NTS cookie exhaustion.
PTP grandmaster changes.
GNSS loss and spoofing.
31.5 Differential testing

Mundilfari should interoperate with and compare against external implementations such as:

chrony.
ntpd.
ntpsec.
linuxptp.
ptp4l.
phc2sys.
gpsd.
reference GNSS tools.
official certification suites.

These programs are test peers, not linked dependencies.

31.6 Hardware laboratory

Before 1.0, testing should include:

Multiple hardware-timestamping NICs.
At least one PTP grandmaster.
Boundary and transparent switches.
PPS source.
GNSS receiver.
IRIG generator.
Radio-clock receiver or captured signal corpus.
White Rabbit-compatible hardware for high-accuracy claims.
Oscillator holdover testing.
Long-running temperature and drift tests.
32. Definition of done for one protocol crate

A protocol is not “implemented” merely when a happy-path packet parses.

A crate is complete when:

The normative specification and revision are recorded.
Applicable errata are recorded.
All message forms are represented.
Strict decoding is complete.
Encoding is complete.
Unknown extensions are preserved where required.
Semantic validation is complete.
Client state machines are complete where applicable.
Server state machines are complete where applicable.
Timing behavior is tested.
Rollover and leap behavior is tested.
Resource limits are documented.
Security considerations are implemented.
Official vectors pass.
Negative tests pass.
Fuzzing finds no panic or memory violation.
Interoperability is demonstrated.
no_std capability is documented.
No third-party dependency has entered the graph.
A diff-focused pentest has passed.
33. Version and publishing policy

All crates use lockstep versions until 1.0.0.

Example:

mundilfari-core 0.74.0
mundilfari-ntp 0.74.0
mundilfari-nts 0.74.0
mundilfari-ptp 0.74.0
mundilfari 0.74.0

A crate may not yet contain a usable implementation at an early workspace version. Its metadata will clearly state its maturity.

33.1 Release gate for every version

Every version below is independently pentestable.

Before tagging any release:

Build every supported target
Build all relevant no_std combinations
Run official and regression vectors
Run malformed-input corpus
Run deterministic fuzzer budget
Review changed unsafe code
Review changed standards mapping
Review resource bounds
Review security impact
Pentest previous tag..HEAD
Fix all critical and high findings
Retest
Sign tag and release evidence

Every tenth minor release additionally performs:

Full-workspace fuzzing.
Full dependency audit.
Full unsafe audit.
Full conformance audit.
Cross-protocol integration run.
34. Detailed roadmap: 0.1.0 to 1.0.0
Phase I — Governance and mathematical foundations
0.1.0   Create workspace, repository policy, licences and crate naming rules.
0.2.0   Add zero-external-dependency manifest guard.
0.3.0   Create the machine-readable Protocol Registry.
0.4.0   Create standards provenance, revision and document-hash system.
0.5.0   Publish the complete initial threat model.
0.6.0   Establish coding, unsafe, panic and integer-overflow policies.
0.7.0   Define no_std, alloc, std and privileged capability levels.
0.8.0   Implement checked signed and unsigned primitive arithmetic.
0.9.0   Implement audited U256 and I256 intermediate arithmetic.
0.10.0  Implement exact fraction conversion and explicit rounding.
0.11.0  Implement signed durations and fixed-point frequency ratios.
0.12.0  Implement typed epochs and epoch conversion framework.
0.13.0  Implement era and rollover resolution framework.
0.14.0  Implement continuous atomic instant representation.
0.15.0  Implement time-scale identifiers and conversion graph.
0.16.0  Implement UTC and positive/negative leap-second model.
0.17.0  Implement Gregorian, Julian, ordinal and ISO-week calendars.
0.18.0  Implement uncertainty intervals and interval arithmetic.
0.19.0  Implement quality, authentication and provenance types.
0.20.0  Core arithmetic and time-model security review.
Phase II — Wire, state-machine, and platform foundations
0.21.0  Implement bounded read and write cursors.
0.22.0  Implement endian, bit-field, BCD and fixed-point codecs.
0.23.0  Implement checksums and CRC framework.
0.24.0  Implement fixed-capacity vector, queue, map and string types.
0.25.0  Implement borrowed/owned packet representation pattern.
0.26.0  Implement protocol poll and timer state-machine framework.
0.27.0  Implement datagram, stream and raw-link transport traits.
0.28.0  Implement clock, entropy, serial and capture traits.
0.29.0  Implement Linux ABI primitive definitions.
0.30.0  Implement Linux TCP and UDP sockets.
0.31.0  Implement raw ICMP and AF_PACKET transports.
0.32.0  Implement zero-dependency DNS resolver and OS-resolver adapter.
0.33.0  Implement blocking executor and Linux epoll reactor.
0.34.0  Implement software socket timestamp capture.
0.35.0  Implement Linux SO_TIMESTAMPING ancillary parsing.
0.36.0  Implement NIC hardware timestamp configuration.
0.37.0  Implement PHC device and cross-timestamp support.
0.38.0  Implement kernel PPS and clock-adjustment support.
0.39.0  Add Windows, BSD, macOS and embedded platform adapters.
0.40.0  Platform, FFI and unsafe-boundary pentest.
Phase III — Legacy services and time representations
0.41.0  Implement RFC 867 Daytime wire and raw-text handling.
0.42.0  Add bounded Daytime parse candidates, client and server.
0.43.0  Implement RFC 868 TIME over TCP and UDP with era handling.
0.44.0  Implement ICMP Timestamp request and reply.
0.45.0  Implement historic DCNET Internet Clock Service.
0.46.0  Implement NIST ACTS modem protocol.
0.47.0  Implement BSD timed/TSP compatibility.
0.48.0  Implement DCE Distributed Time Service compatibility.
0.49.0  Implement documented Microsoft SNTP extensions.
0.50.0  Implement XMPP Entity Time.
0.51.0  Implement HTTP-date and mail-date formats.
0.52.0  Implement ASN.1 UTCTime and GeneralizedTime.
0.53.0  Implement RFC 3339.
0.54.0  Implement RFC 9557 IXDTF.
0.55.0  Implement licensed ISO 8601 profiles required by the registry.
0.56.0  Implement RFC 9636 TZif.
0.57.0  Implement RFC 7808 TZDIST client and server state machines.
0.58.0  Implement DHCPv4 and DHCPv6 NTP discovery options.
0.59.0  Implement leap, IERS and Earth-orientation data loaders.
0.60.0  Legacy and representation suite pentest.
Phase IV — NTP and SNTP
0.61.0  Implement historical and current NTP base headers.
0.62.0  Implement NTP timestamps, eras, reference identifiers and fixed point.
0.63.0  Implement historical and current SNTP client behavior.
0.64.0  Implement SNTP server behavior.
0.65.0  Implement RFC 7821 and RFC 7822 extension handling.
0.66.0  Implement full NTP client exchange validation.
0.67.0  Implement NTP clock filter.
0.68.0  Implement candidate interval and intersection algorithm.
0.69.0  Implement clustering and source combining.
0.70.0  Implement NTP poll, reachability and association state.
0.71.0  Implement PLL, FLL and hybrid discipline foundations.
0.72.0  Deliver complete NTPv4 client.
0.73.0  Deliver complete NTPv4 server.
0.74.0  Implement symmetric active and passive modes.
0.75.0  Implement broadcast and multicast compatibility.
0.76.0  Implement KoD, rate limiting and port randomization.
0.77.0  Implement RFC 9769 interleaved modes.
0.78.0  Implement RFC 9327 mode 6 control protocol.
0.79.0  Implement Autokey parsing and disabled-by-default compatibility.
0.80.0  Implement RFC 9523 Khronos watchdog.
0.81.0  Implement version-pinned NTPv5 draft codec and client.
0.82.0  Implement version-pinned NTP-over-PTP draft.
0.83.0  Complete NTP simulator and differential interoperability.
0.84.0  NTP-family security and conformance pentest.
Phase V — Cryptography, X.509, and TLS
0.85.0   Implement constant-time primitives and secret containers.
0.86.0   Implement SHA-256 and SHA-384.
0.87.0   Implement HMAC and HKDF.
0.88.0   Implement portable and accelerated AES.
0.89.0   Implement AES-CMAC.
0.90.0   Implement AES-SIV-CMAC.
0.91.0   Implement AES-GCM.
0.92.0   Implement ChaCha20 and Poly1305.
0.93.0   Implement ChaCha20-Poly1305.
0.94.0   Implement X25519.
0.95.0   Implement Ed25519 verification and signing.
0.96.0   Implement P-256 and P-384 arithmetic.
0.97.0   Implement ECDSA verification and signing.
0.98.0   Implement bounded big integers and RSA verification.
0.99.0   Implement RSA-PSS and required certificate signatures.
0.100.0  Implement strict ASN.1 DER.
0.101.0  Implement X.509 certificate parsing.
0.102.0  Implement certificate-path construction and validation.
0.103.0  Implement PEM and key-container parsing.
0.104.0  Implement TLS 1.3 record layer.
0.105.0  Implement TLS 1.3 handshake and key schedule.
0.106.0  Implement TLS service identity, SNI and ALPN.
0.107.0  Implement TLS server, tickets and bounded resumption.
0.108.0  Complete TLS interoperability and malformed-input testing.
0.109.0  Independent cryptographic and TLS audit gate.
Phase VI — NTS, Roughtime, and secure bootstrap
0.110.0  Implement NTS-KE client.
0.111.0  Implement NTS-KE server.
0.112.0  Implement NTS-protected NTP client.
0.113.0  Implement NTS-protected NTP server and cookie rotation.
0.114.0  Implement experimental NTS pool extensions.
0.115.0  Implement version-pinned Roughtime client and verifier.
0.116.0  Implement Roughtime server and inconsistency evidence.
0.117.0  Implement secure certificate-time bootstrap state machine.
0.118.0  Implement authenticated multi-protocol interval consensus.
0.119.0  Implement persistent trusted-clock snapshot and recovery.
0.120.0  NTS, Roughtime and bootstrap pentest.
Phase VII — GNSS, pulse, and physical timecodes
0.121.0  Implement complete bounded NMEA 0183 codec.
0.122.0  Implement NMEA 2000 time-related PGNs.
0.123.0  Implement GPS navigation-time messages and rollovers.
0.124.0  Implement Galileo time and OSNMA verification.
0.125.0  Implement BeiDou time messages.
0.126.0  Implement GLONASS time messages.
0.127.0  Implement QZSS, NavIC and SBAS time messages.
0.128.0  Implement RTCM time-related messages.
0.129.0  Implement RINEX time records.
0.130.0  Implement CGGTTS and TWSTFT exchange formats.
0.131.0  Implement documented vendor GNSS protocol crates.
0.132.0  Implement GNSS and PPS correlation engine.
0.133.0  Implement complete selected IRIG revision.
0.134.0  Implement IEEE 1344 and power-system IRIG extensions.
0.135.0  Implement WWVB amplitude and phase codes.
0.136.0  Implement WWV, WWVH and CHU codes.
0.137.0  Implement DCF77, MSF, JJY and other registry radio codes.
0.138.0  Implement eLoran time observations.
0.139.0  Implement physical-source spoof and inconsistency monitoring.
0.140.0  GNSS, PPS, IRIG and radio hardware-in-loop pentest.
Phase VIII — PTP, gPTP, profiles, and White Rabbit
0.141.0  Implement IEEE 1588-2002 compatibility.
0.142.0  Implement IEEE 1588-2008 and 1588-2019 wire formats.
0.143.0  Implement PTP datasets and BMCA.
0.144.0  Implement end-to-end delay mechanism.
0.145.0  Implement peer-to-peer delay mechanism.
0.146.0  Implement one-step and two-step behavior.
0.147.0  Implement raw Ethernet, UDPv4 and UDPv6 transports.
0.148.0  Implement ordinary-clock state machine.
0.149.0  Implement boundary-clock state machine.
0.150.0  Implement end-to-end and peer-to-peer transparent clocks.
0.151.0  Implement signaling, management and YANG mappings.
0.152.0  Integrate Linux hardware timestamps and PHC discipline.
0.153.0  Implement PTP-oriented servo and holdover.
0.154.0  Implement IEEE 802.1AS-2011 and 802.1AS-2020 gPTP.
0.155.0  Implement IETF Enterprise Profile.
0.156.0  Implement ITU-T telecom profiles.
0.157.0  Implement Synchronous Ethernet timing messaging.
0.158.0  Implement power-system PTP profiles.
0.159.0  Implement broadcast, AES67 and fronthaul profiles.
0.160.0  Implement White Rabbit/high-accuracy profile and calibration.
0.161.0  Implement experimental NTS4PTP and PTP security monitoring.
0.162.0  PTP profile conformance and hardware-in-loop pentest.
Phase IX — Industrial, automotive, wireless, media, and space
0.163.0  Implement BACnet time services.
0.164.0  Implement DNP3 time services.
0.165.0  Implement IEC 60870 and IEC 61850 time mappings.
0.166.0  Implement CANopen and J1939 time services.
0.167.0  Implement EtherCAT distributed-clock interfaces.
0.168.0  Implement PROFINET time interfaces.
0.169.0  Implement CIP Sync and other registry industrial profiles.
0.170.0  Implement AUTOSAR Ethernet, CAN and FlexRay time protocols.
0.171.0  Implement native FlexRay and Time-Triggered Ethernet timing.
0.172.0  Implement Bluetooth time services and Mesh Time.
0.173.0  Implement Zigbee, Matter and LoRaWAN time services.
0.174.0  Implement Wi-Fi TSF/FTM and 802.15.4/TSCH timing.
0.175.0  Implement WirelessHART, ISA100, Thread and 6TiSCH timing.
0.176.0  Implement cellular NITZ and 5G reference-time mappings.
0.177.0  Implement SMPTE, MIDI, RDS, DVB, ATSC and ISDB timing.
0.178.0  Implement RTP, MPEG, DASH, HLS and SCTE timing.
0.179.0  Implement CCSDS, SpaceWire and SpaceFibre timecodes.
0.180.0  Industrial, wireless, media and space pentest.
Phase X — Trusted timestamping and evidence
0.181.0  Implement RFC 3161 request, response and TSA server.
0.182.0  Implement RFC 5816 update behavior.
0.183.0  Implement Evidence Record Syntax.
0.184.0  Implement XML Evidence Record Syntax.
0.185.0  Implement timestamped-data binding.
0.186.0  Implement COSE timestamp-header support.
0.187.0  Implement applicable ETSI timestamp profiles.
0.188.0  Implement ANSI X9.95 profile.
0.189.0  Implement Authenticode timestamp compatibility.
0.190.0  Implement OpenTimestamps verification and generation.
0.191.0  Implement evidence-chain policy and archival renewal.
0.192.0  Trusted timestamping and evidence pentest.
Phase XI — Unified product APIs and applications
0.193.0  Freeze unified Source, TimeReading and Clock traits.
0.194.0  Implement easy blocking one-shot query APIs.
0.195.0  Implement fixed-storage no_alloc builders.
0.196.0  Implement Future and poll adapters.
0.197.0  Implement TrustedClock.
0.198.0  Implement cross-protocol consensus and holdover engine.
0.199.0  Implement mundilfarid synchronization daemon.
0.200.0  Implement minimal privileged clock helper.

At this point all planned protocol functionality exists, but the stable release has not yet been declared.

The stabilization sequence continues without introducing new protocol scope:

0.201.0  Complete multi-protocol server framework.
0.202.0  Complete CLI query, inspect, compare, decode and convert commands.
0.203.0  Complete CLI serve, discipline, monitor and audit commands.
0.204.0  Complete C ABI.
0.205.0  Complete WASM and browser-safe APIs.
0.206.0  Complete metrics, health and audit-record interfaces.
0.207.0  Complete configuration and policy language.
0.208.0  Complete network and oscillator simulator.
0.209.0  Complete internal deterministic fuzzer.
0.210.0  Complete examples and deployment documentation.
Phase XII — Final hardening
0.211.0  Close all official-vector gaps.
0.212.0  Complete differential interoperability matrix.
0.213.0  Complete full-workspace unsafe review.
0.214.0  Complete constant-time and side-channel review.
0.215.0  Complete parser and resource-exhaustion review.
0.216.0  Complete downgrade and trust-bootstrap review.
0.217.0  Complete fault-injection and long-duration holdover tests.
0.218.0  Complete performance, latency and memory benchmarks.
0.219.0  Complete supported-target and no_std matrix.
0.220.0  Close Protocol Registry stable-scope gaps.
0.221.0  Complete standards, errata and licence refresh.
0.222.0  Freeze public APIs.
0.223.0  Freeze wire-compatibility guarantees.
0.224.0  Independent cryptographic audit.
0.225.0  Independent protocol and daemon security audit.
0.226.0  Full workspace pentest.
0.227.0  Beta 1; no new features.
0.228.0  Beta 2; compatibility and documentation fixes only.
0.229.0  Release Candidate 1.
0.230.0  Release Candidate 2 and final reproducibility audit.
Version 1.0.0

1.0.0 is tagged only when:

All stable-baseline registry entries are complete or explicitly documented as impossible due to unavailable specifications.
Every published crate has a conformance statement.
Every default-enabled protocol has passed security review.
Cryptography and TLS have received independent review.
There are no known critical or high-severity vulnerabilities.
No third-party Cargo dependency exists.
All claimed no_std configurations build.
Linux daemon privilege separation has passed pentesting.
PTP and physical-source accuracy claims have hardware evidence.
Draft protocols remain isolated from stable APIs.
Documentation clearly differentiates authenticated, accurate, traceable, and merely formatted time.
Reproducible release artifacts and signed evidence are published.
35. Post-1.0 policy

New standards published after the baseline date enter 1.x.

Examples:

1.1.0   Newly finalized Roughtime RFC migration
1.2.0   Finalized NTP-over-PTP RFC
1.3.0   Finalized NTS-for-PTP RFC
1.4.0   Finalized NTPv5 RFC

Draft-to-RFC migration rules:

Retain the old draft decoder under a compatibility feature.
Add the final RFC as a distinct protocol revision.
Do not reinterpret stored draft packets as final RFC packets.
Provide explicit migration notes.
Never silently change cryptographic transcript or wire behavior.

Security fixes receive patch releases and backports according to a published support policy.

36. Final recommendation

Mundilfari should position itself as:

A zero-dependency, no_std-first, security-focused framework for time representation, transfer, synchronization, discipline, verification, and evidence across software, networks, hardware, radio, GNSS, industrial systems, and precision timing.

The project’s strongest architectural principles should be:

Preserve native protocol meaning.
Never confuse UTC, POSIX, TAI, GNSS, PTP, or monotonic time.
Treat uncertainty as data.
Separate authentication from accuracy.
Separate packet parsing from policy and I/O.
Keep protocol cores no_std.
Require no external Rust crates.
Never silently fall back to an insecure protocol.
Never adjust a privileged clock without explicit policy.
Follow exact official specifications, revisions, and errata.
Keep active drafts version-pinned and experimental.
Make every release small, reviewable, and pentestable.
Preserve raw evidence for diagnostics and forensics.
Refuse to claim conformance or precision without evidence.
Delay 1.0.0 until the complete registry baseline is genuinely usable.

This plan intentionally ends at 0.230.0 before 1.0.0: the last twenty releases introduce no protocol features and are reserved for integration, audits, pentesting, conformance closure, and API stabilization.

i am just thinking it is pointless to go implement tls so lets say as minimal crates as possible just nothing that is core related to the time protocols itself that we build. but we could maybe use rusttls if you agree.
Worked for 3m 37s
Yes—this is the correct architectural change

Implementing TLS, X.509 validation, certificate-path building, cryptographic primitives, and random-number generation would turn Mundilfari into two enormous projects:

An ultimate time-protocol framework.
A new general-purpose cryptographic and TLS ecosystem.

The second project would consume years of work while making Mundilfari harder—not easier—to trust. Mundilfari should implement everything specific to time protocols, but reuse carefully selected implementations of generic security and operating-system functionality.

The crate is spelled Rustls, although the package name is rustls.

Revised dependency principle

The new rule should be:

Mundilfari owns all time semantics, time-protocol wire formats, validation, state machines, algorithms, clock discipline, source selection, and security policy. It may use audited external crates for mature generic primitives that are not intrinsically time protocols.

Mundilfari must implement itself
Time and duration representations.
Epochs, eras and rollover resolution.
UTC, TAI, GPS, PTP and other time-scale conversions.
Leap-second handling.
Uncertainty and traceability.
NTP packet parsing and serialization.
NTP extension fields.
SNTP behavior.
NTP filtering, selection, clustering and combining.
Khronos behavior.
NTS-KE record parsing and serialization.
NTS cookies and cookie-jar state.
NTS extension-field construction.
NTS key-exporter context construction.
PTP messages, datasets, BMCA and port state machines.
PTP profiles.
GNSS, NMEA, IRIG and radio protocol decoding.
Clock servos and holdover.
Protocol servers and clients.
Security validation specific to each time standard.
Mundilfari should not implement itself
TLS.
X.509.
General certificate-path validation.
AES.
SHA-2.
Ed25519.
ECDSA.
RSA.
Generic AEAD constructions.
Operating-system ABI declarations where a maintained platform crate is suitable.
A general asynchronous runtime.
A general serialization framework.

The important boundary is that Mundilfari still implements NTS, while Rustls merely supplies the TLS channel used by one phase of NTS.

How Rustls fits NTS

RFC 8915 requires NTS Key Establishment to use TLS 1.3 or newer, requires ALPN negotiation using ntske/1, and derives the NTP client-to-server and server-to-client keys through the TLS exporter using the label EXPORTER-network-time-security.

Rustls is particularly suitable because it provides:

TLS 1.3 client and server support.
ALPN configuration and negotiated-protocol inspection.
TLS exporter key-material generation.
Certificate verification.
Pluggable cryptographic providers.
Buffered and unbuffered connection APIs.

Therefore the architecture should be:

Mundilfari NTS implementation
├── Constructs NTS-KE request records
├── Asks Rustls to establish TLS 1.3
├── Verifies ALPN == "ntske/1"
├── Sends and receives NTS-KE application data
├── Parses the NTS-KE response itself
├── Selects the negotiated NTP and AEAD parameters
├── Constructs the RFC 8915 exporter contexts
├── Asks Rustls to export C2S and S2C key material
├── Stores cookies and negotiated state
└── Protects subsequent NTP packets itself

Rustls must not parse NTS records or construct NTS packet extensions. Those remain Mundilfari responsibilities.

Do not create a separate Rustls adapter crate

Because you want as few crates as reasonably possible, I would not create:

mundilfari-nts-core
mundilfari-nts-wire
mundilfari-nts-rustls
mundilfari-nts-client
mundilfari-nts-server

Use one crate:

mundilfari-nts

Internally:

mundilfari-nts/
└── src/
    ├── lib.rs
    ├── record.rs
    ├── codec.rs
    ├── negotiation.rs
    ├── exporter.rs
    ├── cookie.rs
    ├── extension.rs
    ├── client.rs
    ├── server.rs
    ├── aead.rs
    └── rustls.rs       # Only compiled with the rustls feature

Conceptual features:

[features]
default = []
alloc = []
std = ["alloc"]
client = []
server = []
rustls = ["std", "dep:rustls"]

This gives two useful configurations:

# Protocol parsing/state only; no Rustls and no std.
mundilfari-nts = {
    version = "...",
    default-features = false
}
# Complete ordinary NTS client using Rustls.
mundilfari-nts = {
    version = "...",
    features = ["client", "rustls"]
}

The base crate remains no_std. Rustls integration becomes optional.

Introduce a TLS abstraction

The NTS state machine should not directly expose Rustls types throughout its public API.

pub trait NtsTlsSession {
    type Error;

    fn negotiated_protocol(&self) -> Option<&[u8]>;

    fn send_application_data(
        &mut self,
        plaintext: &[u8],
    ) -> Result<(), Self::Error>;

    fn receive_application_data(
        &mut self,
        output: &mut [u8],
    ) -> Result<usize, Self::Error>;

    fn export_keying_material(
        &self,
        label: &[u8],
        context: &[u8],
        output: &mut [u8],
    ) -> Result<(), Self::Error>;
}

Mundilfari supplies:

#[cfg(feature = "rustls")]
pub struct RustlsNtsSession {
    // Rustls connection and TCP transport.
}

This allows advanced users to integrate another TLS implementation without changing the NTS protocol engine.

NTS still needs a generic AEAD implementation

Rustls solves the NTS-KE TLS phase, but it does not eliminate the cryptography required in subsequent UDP NTP messages.

RFC 8915 requires NTS servers to support AEAD_AES_SIV_CMAC_256, identifier 15, for NTS-protected NTPv4 traffic.

Mundilfari should not write AES or AES-SIV itself. A reasonable candidate is the RustCrypto aes-siv implementation, which implements RFC 5297 AES-CMAC-SIV.

Mundilfari still owns:

AEAD algorithm negotiation.
Construction of associated data.
Nonce fields.
Ciphertext and padding layout.
Directional C2S and S2C keys.
Extension ordering.
Cookie-key rotation.
Authentication-failure behavior.
NTS NAK handling.

The dependency only performs the generic cryptographic operation.

Rustls cryptographic provider policy

Rustls currently supports two built-in provider choices:

aws-lc-rs, the default.
ring, available through an optional feature.

It also supports custom providers.

Mundilfari’s library should not force one provider. The application should choose:

mundilfarid with aws-lc-rs
Embedded gateway with ring
Enterprise application with an approved custom provider

The high-level mundilfarid binary can select one tested default, while mundilfari-nts accepts an application-provided Rustls configuration.

I would not use rustls-rustcrypto as the production default yet. Its current documentation labels it alpha, incomplete, and unsuitable for production use.

Revised minimal shared-crate structure

The earlier architecture had too many tiny foundation crates. Reduce it to:

mundilfari
mundilfari-core
mundilfari-platform
mundilfari-engine

Then retain one crate per actual protocol or major protocol family:

mundilfari-daytime
mundilfari-time
mundilfari-icmp-time
mundilfari-ntp
mundilfari-sntp
mundilfari-nts
mundilfari-roughtime
mundilfari-ptp
mundilfari-gptp
mundilfari-white-rabbit
mundilfari-nmea0183
mundilfari-irig
...
mundilfari-core

Contains:

All common time types.
Calendars.
Time scales.
Leap seconds.
Uncertainty.
Provenance.
Bounded buffers.
Wire cursors.
Checksums and CRC utilities.
Common transport and clock traits.
mundilfari-platform

Contains:

Standard sockets.
Linux raw sockets.
Linux hardware timestamps.
PHC and PPS access.
System-clock adjustment.
Windows, BSD and macOS platform integration.

Using libc and windows-sys here is reasonable. Kernel ABI declarations are not time-protocol logic, and maintaining handwritten copies creates unnecessary portability and safety risk.

mundilfari-engine

Contains:

Multi-source consensus.
NTP-style source selection.
Clock servos.
Holdover.
Virtual trusted clocks.
Daemon orchestration.
Clock-discipline policy.
mundilfari

Contains:

Easy facade.
Re-exports.
Builders.
Unified client and server APIs.
Dependencies that should remain forbidden

Even after relaxing the policy, Mundilfari should not become dependency-heavy.

Avoid dependencies that replace the project’s actual purpose:

chrono/time        Time representation is Mundilfari’s core.
nom                Protocol parsing is Mundilfari’s core.
byteorder          Wire handling is Mundilfari’s core.
ntp crates         NTP is Mundilfari’s core.
ptp crates         PTP is Mundilfari’s core.
nmea parsers       NMEA time decoding is Mundilfari’s core.
tokio by default   Not required for the protocol engines.
serde by default   Not needed in core protocol crates.

Allow dependencies only for tightly bounded generic functionality:

rustls             TLS for NTS-KE.
AES-SIV            Mandatory NTS AEAD.
Signature/hash
implementations    Roughtime, GNSS authentication and timestamp evidence.
libc/windows-sys   Operating-system bindings.

Every dependency should be:

Optional wherever possible.
Disabled from default no_std builds.
Version-pinned in application lockfiles.
Included in the threat model and SBOM.
Audited for enabled features and transitive dependencies.
Replaceable behind a Mundilfari trait.
Updated promptly for security releases.
Roadmap correction

The previous releases dedicated to implementing TLS and generic cryptography should be removed:

REMOVE:
0.85.0–0.109.0 custom cryptography, ASN.1, X.509 and TLS

Replace them with:

0.85.0  Establish external cryptography dependency policy.
0.86.0  Add generic AEAD and signature-provider traits.
0.87.0  Implement complete NTS-KE record codecs.
0.88.0  Implement NTS-KE client state machine.
0.89.0  Integrate Rustls TLS 1.3 and ALPN.
0.90.0  Integrate TLS exporter key derivation.
0.91.0  Integrate AES-SIV-CMAC-256.
0.92.0  Implement NTS-protected NTP client.
0.93.0  Implement NTS cookie handling and persistence.
0.94.0  Implement NTS-KE server.
0.95.0  Implement NTS-protected NTP server.
0.96.0  Complete Rustls and NTS interoperability testing.
0.97.0  Complete NTS security review and pentest.

This probably removes several years of unrelated work while producing a safer and more credible 1.0.0.

The final philosophy should therefore be:

Mundilfari builds every part that gives time protocols their meaning. It does not rebuild mature generic infrastructure merely to claim zero dependencies.

just to be clear is this project implementing full gps? or it is just time related not coordinates correct?

Correct: Mundilfari is not intended to be a complete GPS/GNSS navigation stack. It should implement only the portions needed for time acquisition, synchronization, validation, and traceability.

For GPS and other GNSS systems, Mundilfari would handle:

GPS time and UTC conversion.
GPS week numbers and rollover resolution.
Leap-second and UTC correction data.
Time-of-week fields.
Receiver clock bias and timing uncertainty.
Satellite and signal identity for provenance.
Navigation-message parity or CRC needed to trust timing data.
PPS and receiver-message correlation.
Receiver health, time-valid, jamming, spoofing, and authentication indicators.
Galileo OSNMA verification where relevant to authenticated time.
NMEA sentences containing time, such as ZDA and RMC.

It would not aim to implement:

Latitude and longitude calculation.
Position, velocity, and altitude solutions.
Trilateration or pseudorange positioning.
Ephemeris-based orbit calculations except where minimally necessary to validate time.
Maps, routing, navigation, geofencing, or geodesy.
RTK positioning or centimeter-level coordinate correction.
A complete GPS receiver or software-defined GNSS receiver.

Some messages, such as NMEA RMC, contain both time and coordinates. Mundilfari may structurally decode or preserve those coordinate fields so that the complete message can be validated, but coordinates should not become part of its main public purpose.

To prevent confusion, I would adjust several crate names:

mundilfari-gps-time
mundilfari-galileo-time
mundilfari-beidou-time
mundilfari-glonass-time
mundilfari-nmea0183-time
mundilfari-nmea2000-time
mundilfari-rtcm-time

A clear project rule would be:

Mundilfari implements GNSS as a source of precise and traceable time, not as a positioning or navigation framework.

A separate future crate could implement full GNSS navigation and reuse Mundilfari for its time subsystem.

no that is good since we have another project navheim where we implement full gps so i not want the two to mixup, this crate is only meant for time protocols
Memory updated

Exactly. The project boundary should be strict:

Mundilfari owns time. Navheim owns navigation.

Mundilfari
Time-transfer and synchronization protocols.
Clock representations, epochs and time scales.
NTP, SNTP, NTS, PTP and gPTP.
PPS, IRIG and radio timecodes.
GNSS-derived time observations.
Leap-second and GNSS week handling.
Receiver timing quality and uncertainty.
Clock discipline, source selection and holdover.
Timestamp verification and trusted-time evidence.
Navheim
GPS/GNSS navigation-message processing.
Coordinates, position, velocity and altitude.
Satellite orbit and ephemeris calculations.
Pseudorange and carrier-phase solutions.
Trilateration.
RTK, PPP and differential corrections.
Geodesy, routes and navigation.
Full GNSS receiver functionality.

For shared GNSS messages, Mundilfari should decode only the fields necessary to obtain and validate time. It may preserve unrelated fields as opaque data, but it should not expose positioning APIs.

A suitable architectural statement for the repository is:

Mundilfari implements GNSS timing, not GNSS navigation. Positioning, coordinates, and full satellite-navigation functionality belong to Navheim.

I would also keep the explicit crate names:

mundilfari-gps-time
mundilfari-galileo-time
mundilfari-glonass-time
mundilfari-beidou-time
mundilfari-nmea0183-time
mundilfari-nmea2000-time

That naming prevents users from mistakenly expecting a complete GPS implementation.

does it mean we need still gps equipment to do those parts?

Not for implementing most of the software, but yes for final real-world validation.

You can build and test much of Mundilfari without GPS equipment using:

Official protocol examples and test vectors.
Recorded NMEA or binary GNSS data.
Recorded PPS timestamps.
Synthetic receiver streams.
Invalid-message and rollover test corpora.
A simulator that generates GPS time, leap-second announcements, week rollovers, signal loss, and spoofing scenarios.

Actual GNSS equipment becomes necessary for testing the hardware-facing parts:

Reading NMEA or vendor messages over serial/USB.
Capturing a physical PPS signal.
Correlating PPS edges with the corresponding GNSS time message.
Measuring serial-message latency and jitter.
Testing Linux /dev/pps* integration.
Testing loss of satellite lock and receiver holdover.
Checking real receiver quality and uncertainty fields.
Comparing GNSS time with NTP, NTS, PTP, or a hardware clock.
Validating Galileo OSNMA or other authenticated navigation-time information from a live receiver.
Minimal Mundilfari GNSS timing lab

You would eventually need only:

GNSS timing receiver with PPS output
Active GNSS antenna
USB or serial connection for time messages
PPS connection to a GPIO, serial-control pin, or timing capture device
Linux test computer
Optional logic analyzer or oscilloscope

This is much smaller than the equipment Navheim may eventually need. Mundilfari does not need enough hardware to calculate coordinates itself; it only needs a receiver that provides:

Precise time message + physical PPS edge + timing quality information

A normal consumer USB GPS dongle may provide NMEA time but often lacks an accessible PPS output. That is enough for parser development, but not enough for serious precision-timing validation.

So the recommended progression is:

Develop all codecs and state machines using test vectors and captured data.
Add an inexpensive receiver that exposes serial data and PPS.
Later add a proper timing-grade receiver for accuracy, holdover, spoofing, and hardware timestamp testing.

Navheim can reuse the same receiver equipment later, but Mundilfari only consumes its timing outputs, never its coordinate solution.

## Final ownership addendum — Navheim determines GNSS time

The earlier timing-only split still duplicated GNSS behavior. Even a
"timing-only" GPS implementation would have required Mundilfari to decode
navigation or receiver messages, resolve truncated weeks, interpret
satellite-transmitted UTC and leap models, apply receiver clock corrections,
evaluate health, verify OSNMA/QZNMA, and correlate receiver time marks with
PPS. Navheim already plans to implement those operations as part of one
complete GNSS/PNT system.

The final boundary is:

**Navheim determines time from GNSS. Mundilfari determines what to do with
that validated time as one source among NTP, NTS, PTP, radio, generic PPS,
hardware clocks, and local oscillators.**

Navheim owns all GNSS-specific timing meaning:

- constellation navigation frames and receiver protocols;
- NMEA, RTCM, RINEX, gpsd, and documented vendor formats;
- native epochs, week/day/era resolution, and transmitted UTC/leap models;
- satellite and receiver clock models and time-only solutions;
- health, OSNMA/QZNMA, spoofing, jamming, replay, integrity, and provenance;
- receiver time-mark, PPS, frequency-output, delay, and uncertainty semantics.

Mundilfari keeps:

- generic continuous/atomic/civil time and named GNSS scale identifiers;
- independent leap/scale models for fail-closed cross-checking;
- generic physical PPS and frequency capture;
- protocol-neutral observations and source traits;
- cross-family comparison, consensus, servos, holdover, and clock discipline.

There will be no `mundilfari-gps-time`, `mundilfari-galileo-time`,
`mundilfari-glonass-time`, `mundilfari-beidou-time`,
`mundilfari-nmea0183-time`, `mundilfari-nmea2000-time`,
`mundilfari-rtcm-time`, or Mundilfari vendor-receiver crate.

After Navheim is built first and publishes a reviewed stable GNSS timing
observation/event API, one optional crates.io companion,
`mundilfari-navheim`, will depend on both projects. Navheim never depends on
Mundilfari, and Mundilfari's default graph never depends on Navheim.

The adapter maps exact instants, uncertainty, capture-domain identity, health,
authentication, integrity, freshness, provenance, and invalidation without
reinterpreting GNSS. Mundilfari's generic source API continues to accept
already validated observations from appliances, SDKs, custom receivers, or
recorded laboratories without claiming GNSS decoding conformance.

Generic PPS capture remains Mundilfari-owned. Navheim owns which GNSS instant
a receiver says that pulse represents. The companion preserves both halves and
never guesses the association.

TWSTFT and other communication-satellite time-transfer protocols remain
Mundilfari work because they are time protocols rather than GNSS navigation
interpretation. Mundilfari may encode/decode CGGTTS interchange records, but
the GNSS common-view/all-in-view solution evidence comes from Navheim.

The implementation roadmap therefore completes all Navheim-independent work
first. Generic satellite observations and TWSTFT do not require Navheim and
remain earlier work. The optional companion, its complete evidence mapping,
GNSS/PPS semantic bridge, and CGGTTS are the final feature phase. Only
whole-system conformance, audits, release candidates, and `1.0.0` follow it.
