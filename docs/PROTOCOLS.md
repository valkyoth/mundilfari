# Mundilfari Protocol Registry

Status: initial planning registry

Baseline date: 2026-07-24

This registry defines the 1.0 completeness claim. Entries are implemented only
from official, legitimately accessible specifications and verified errata.
Licensed text is not redistributed without permission.

## Status Vocabulary

| Status | Meaning |
| --- | --- |
| `PlannedStable` | public stable specification in the pre-1.0 scope |
| `PlannedHistorical` | obsolete/historic interoperability; disabled by secure defaults |
| `ExperimentalPinned` | active draft with revision-specific experimental API |
| `LicenceRequired` | known normative standard requires legitimate licensed access |
| `SpecificationRequested` | official text/access still being located |
| `KnownUnavailable` | known but inaccessible; no implementation claim |
| `ProprietaryUndocumented` | no public normative specification; not guessed |
| `TimingOnly` | only time-related services are in scope |
| `ExternalNavheim` | owned by Navheim and consumed only through the companion adapter |

Every implementation adds exact identifiers, revisions, publication dates,
official URLs, errata, clause maps, test-vector provenance, and conformance
level to the machine-readable registry introduced by the release plan.

## Internet Time And Discovery

| Crate/family | Standard or protocol | Status |
| --- | --- | --- |
| `mundilfari-daytime` | RFC 867 Daytime | `PlannedHistorical` |
| `mundilfari-time` | RFC 868 TIME | `PlannedHistorical` |
| `mundilfari-icmp-time` | ICMP Timestamp Request/Reply | `PlannedHistorical` |
| `mundilfari-dcnet-clock` | DCNET Internet Clock Service | `PlannedHistorical` |
| `mundilfari-nist-acts` | NIST ACTS | `PlannedHistorical` |
| `mundilfari-bsd-timed` | BSD timed/TSP | `PlannedHistorical` |
| `mundilfari-dce-dts` | DCE Distributed Time Service | `SpecificationRequested` |
| `mundilfari-ms-sntp` | Microsoft SNTP extensions | `PlannedStable` |
| `mundilfari-xmpp-time` | XMPP Entity Time | `PlannedStable` |
| `mundilfari-ntp-discovery` | DHCP and configured NTP discovery | `PlannedStable` |
| `mundilfari-ntp-management` | NTP MIB/YANG management mappings | `PlannedStable` |

## NTP Family

| Crate/family | Standard or protocol | Status |
| --- | --- | --- |
| `mundilfari-ntp-wire` | shared NTP headers and extension fields | `PlannedStable` |
| `mundilfari-ntp-legacy` | NTPv0-v3 compatibility | `PlannedHistorical` |
| `mundilfari-sntp` | historical/current SNTP behavior | `PlannedStable` |
| `mundilfari-ntp` | full NTPv4 client/server/association engine | `PlannedStable` |
| `mundilfari-ntp-control` | mode 6 control | `PlannedStable` |
| `mundilfari-ntp-autokey` | Autokey inspection/compatibility | `PlannedHistorical` |
| `mundilfari-ntp-khronos` | RFC 9523 Khronos | `PlannedStable` |
| `mundilfari-nts` | RFC 8915 Network Time Security | `PlannedStable` |
| `mundilfari-ntpv5` | exact active NTPv5 draft | `ExperimentalPinned` |
| `mundilfari-ntp-over-ptp` | exact IETF draft | `ExperimentalPinned` |
| `mundilfari-nts4ptp` | exact NTS-for-PTP draft | `ExperimentalPinned` |

## Secure Time And Timestamp Evidence

| Crate/family | Standard or protocol | Status |
| --- | --- | --- |
| `mundilfari-roughtime` | exact IETF Roughtime revision/final RFC | `ExperimentalPinned` |
| `mundilfari-rfc3161` | RFC 3161 Time-Stamp Protocol | `PlannedStable` |
| `mundilfari-rfc5816` | RFC 5816 update | `PlannedStable` |
| `mundilfari-ers` | Evidence Record Syntax | `PlannedStable` |
| `mundilfari-xmlers` | XML Evidence Record Syntax | `PlannedStable` |
| `mundilfari-timestamped-data` | timestamped-data binding | `PlannedStable` |
| `mundilfari-cose-timestamp` | COSE timestamp headers | `PlannedStable` |
| `mundilfari-etsi-timestamp` | applicable ETSI profiles | `LicenceRequired` |
| `mundilfari-x995` | ANSI X9.95 profile | `LicenceRequired` |
| `mundilfari-authenticode-time` | Authenticode timestamp compatibility | `PlannedStable` |
| `mundilfari-opentimestamps` | OpenTimestamps | `PlannedStable` |

Timestamp evidence proves a time assertion about data. It is not a replacement
for a continuously synchronized local clock.

## Precision Time And Frequency

| Crate/family | Standard or protocol | Status |
| --- | --- | --- |
| `mundilfari-ptp-wire` | shared PTP wire formats | `LicenceRequired` |
| `mundilfari-ptp-v1` | IEEE 1588-2002 | `LicenceRequired` |
| `mundilfari-ptp` | IEEE 1588-2008/2019 | `LicenceRequired` |
| `mundilfari-gptp` | IEEE 802.1AS-2011/2020 | `LicenceRequired` |
| `mundilfari-ptp-enterprise` | IETF Enterprise Profile | `PlannedStable` |
| `mundilfari-ptp-telecom` | ITU-T G.8265.1/G.8275.1/G.8275.2 | `LicenceRequired` |
| `mundilfari-ptp-power` | IEEE C37.238, IEC/IEEE 61850-9-3 | `LicenceRequired` |
| `mundilfari-ptp-media` | SMPTE ST 2059-2, AES67 | `LicenceRequired` |
| `mundilfari-ptp-fronthaul` | IEEE 802.1CM/O-RAN timing | `LicenceRequired` |
| `mundilfari-white-rabbit` | White Rabbit/high-accuracy profile | `LicenceRequired` |
| `mundilfari-synce` | Synchronous Ethernet messaging/quality | `LicenceRequired` |

## GNSS-Derived And Satellite Timing

Mundilfari implements no GNSS navigation-message or receiver-protocol decoder.
Navheim is the planned upstream for every GNSS constellation and format. One
companion crate maps its complete timing evidence into Mundilfari without
reinterpreting it.

| Crate/family | Time source/protocol | Status |
| --- | --- | --- |
| `mundilfari-navheim` | all validated Navheim GNSS timing observations/events | `ExternalNavheim` |
| Navheim upstream | GPS, Galileo, BeiDou, GLONASS, QZSS, NavIC, SBAS | `ExternalNavheim` |
| Navheim upstream | NMEA 0183/2000, RTCM, RINEX, gpsd and vendor receivers | `ExternalNavheim` |
| Navheim upstream | OSNMA/QZNMA, GNSS PPS meaning and common/all-in-view transfer | `ExternalNavheim` |
| generic source API | validated observations from appliances, SDKs or custom receivers | `PlannedStable` |
| `mundilfari-cggtts` | CGGTTS interchange over validated GNSS transfer evidence | `PlannedStable` |
| `mundilfari-twstft` | two-way communication-satellite time/frequency transfer | `LicenceRequired` |

TWSTFT remains here because it is a time-transfer protocol over communication
satellites, not GNSS navigation interpretation. Any GNSS receiver semantics or
common-view result enters through Navheim. CGGTTS owns only the exchange
format; it consumes already validated transfer evidence and performs no GNSS
solution or receiver interpretation.

## Pulse, Serial, Radio, And Physical Timecodes

| Crate/family | Protocol/source | Status |
| --- | --- | --- |
| `mundilfari-pps` | generic physical pulse capture and quality | `PlannedStable` |
| `mundilfari-frequency-reference` | frequency reference observation | `PlannedStable` |
| `mundilfari-irig` | selected complete IRIG revision | `LicenceRequired` |
| `mundilfari-ieee1344` | IEEE 1344 extensions | `LicenceRequired` |
| radio time crates | WWVB, WWV/WWVH, CHU, DCF77, MSF, JJY | `PlannedStable` |
| radio time crates | BPC, ALS162, RWM, BPM | `SpecificationRequested` |
| `mundilfari-eloran` | eLoran timing | `LicenceRequired` |

## Broadcast, Media, And Web Timing

| Crate/family | Protocol | Status |
| --- | --- | --- |
| `mundilfari-smpte-timecode` | SMPTE timecode | `LicenceRequired` |
| `mundilfari-midi-timecode` | MIDI timecode | `LicenceRequired` |
| `mundilfari-aes-time` | AES audio timing | `LicenceRequired` |
| broadcast time crates | RDS, DVB, ATSC, ISDB | `LicenceRequired` |
| `mundilfari-rtp-time` | RTP/RTCP clock correlation | `PlannedStable` |
| `mundilfari-mpeg-time` | PTS/DTS/PCR timing | `LicenceRequired` |
| web media time crates | DASH, HLS, SCTE | `LicenceRequired` |

Media counters are not UTC without an explicit clock correlation.

## Space Systems

| Crate/family | Protocol | Status |
| --- | --- | --- |
| `mundilfari-ccsds-time` | CCSDS time-code families | `LicenceRequired` |
| `mundilfari-spacewire-time` | SpaceWire time codes | `LicenceRequired` |
| `mundilfari-spacefibre-time` | SpaceFibre time distribution | `LicenceRequired` |
| `mundilfari-ecss-time` | ECSS timing profiles | `LicenceRequired` |

## Industrial, Energy, And Building Timing

All are `TimingOnly`: Mundilfari implements time services, not the surrounding
complete industrial stack.

| Family | Protocols | Status |
| --- | --- | --- |
| building/utility | BACnet, DNP3 | `LicenceRequired` |
| power automation | IEC 60870, IEC 61850 | `LicenceRequired` |
| vehicle/field bus | CANopen, J1939 | `LicenceRequired` |
| industrial Ethernet | EtherCAT, PROFINET, CIP Sync, Sercos, POWERLINK | `LicenceRequired` |
| building/industrial apps | KNX, OPC UA | `LicenceRequired` |

## Automotive And Deterministic Networks

| Family | Protocols | Status |
| --- | --- | --- |
| AUTOSAR | Ethernet, CAN, FlexRay time synchronization | `LicenceRequired` |
| deterministic bus | FlexRay, SAE AS6802/TTEthernet | `LicenceRequired` |
| TSN/fronthaul | TSN and O-RAN timing profiles | `LicenceRequired` |

## Wireless, IoT, And Cellular

| Family | Protocols | Status |
| --- | --- | --- |
| Bluetooth | Current Time, Reference Time Update, Device Time, Mesh Time | `LicenceRequired` |
| IoT | Zigbee, Matter, LoRaWAN DeviceTime | `LicenceRequired` |
| Wi-Fi | TSF, FTM and clock correlation | `LicenceRequired` |
| low-power deterministic | TSCH, 6TiSCH, WirelessHART, ISA100, Thread | `LicenceRequired` |
| cellular | NITZ and 5G reference-time mappings | `LicenceRequired` |

Local network synchronization is not labeled UTC without a civil-time
correlation.

## Time Representation, Zone, And Discovery

| Crate/family | Standard | Status |
| --- | --- | --- |
| `mundilfari-rfc3339` | RFC 3339 | `PlannedStable` |
| `mundilfari-ixdtf` | RFC 9557 IXDTF | `PlannedStable` |
| `mundilfari-iso8601` | licensed ISO 8601 profiles | `LicenceRequired` |
| `mundilfari-http-date` | HTTP and mail date formats | `PlannedStable` |
| `mundilfari-asn1-time` | UTCTime and GeneralizedTime | `PlannedStable` |
| `mundilfari-tzif` | RFC 9636 TZif | `PlannedStable` |
| `mundilfari-tzdist` | RFC 7808 TZDIST | `PlannedStable` |
| `mundilfari-posix-tz` | POSIX TZ representation | `PlannedStable` |
| `mundilfari-ical-timezone` | iCalendar time-zone components | `PlannedStable` |

## Completeness Review Rule

Every planning, standards-refresh, and pentest pass must ask:

1. Has a public time-transfer, synchronization, timecode, discovery,
   representation, or trusted-timestamp standard been omitted?
2. Did a draft become an RFC or stable standard?
3. Did an erratum, revision, registry update, or security BCP change behavior?
4. Is the normative text legitimately available?
5. Is the entry assigned to a pre-1.0 milestone?
6. Are non-claims and navigation boundaries still explicit?

Newly discovered stable pre-baseline work is assigned before `1.0.0`, even if
that requires versions beyond the current plan.
