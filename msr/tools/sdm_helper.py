#!/usr/bin/env python
"""Helper script for processing RAPL data from Intel Software Developer's Manual, Volume 4."""

import sys

__author__ = "Connor Imes"
__date__ = "2018-04-19"


MSR_RAPL_POWER_UNIT = "MSR_RAPL_POWER_UNIT" # 0x606
MSR_PKG_POWER_LIMIT = "MSR_PKG_POWER_LIMIT" # 0x610
MSR_PKG_ENERGY_STATUS = "MSR_PKG_ENERGY_STATUS" # 0x611
MSR_PP0_POWER_LIMIT = "MSR_PP0_POWER_LIMIT" # 0x638
MSR_PP0_ENERGY_STATUS = "MSR_PP0_ENERGY_STATUS" # 0x639
MSR_PP1_POWER_LIMIT = "MSR_PP1_POWER_LIMIT" # 0x640
MSR_PP1_ENERGY_STATUS = "MSR_PP1_ENERGY_STATUS" # 0x641
MSR_DRAM_POWER_LIMIT = "MSR_DRAM_POWER_LIMIT" # 0x618
MSR_DRAM_ENERGY_STATUS = "MSR_DRAM_ENERGY_STATUS" # 0x619
MSR_PLATFORM_POWER_LIMIT = "MSR_PLATFORM_POWER_LIMIT" # 0x65C
MSR_PLATFORM_ENERGY_COUNTER = "MSR_PLATFORM_ENERGY_COUNTER" # 0x64D

NONE = "None"
POWER_DEFAULT = "14.9.1"
PKG_DEFAULT = "14.9.3"
PP0_DEFAULT = "14.9.4"
PP1_DEFAULT = "14.9.4"
DRAM_DEFAULT = "14.9.5"
PLATFORM_DEFAULT = "Table 2-38"
DRAM_15_3 = "ESU: 15.3 uJ" # assumed for now that this ESU is found in MSR_RAPL_POWER_UNIT
RESERVED = "Reserved (0)" # this should also be OK (just gets a 0 energy reading)


class CPU(object):
    """A CPU with RAPL register info in a list of tables."""

    DELIM = '\t'

    REGS = [MSR_RAPL_POWER_UNIT,
            MSR_PKG_POWER_LIMIT, MSR_PKG_ENERGY_STATUS,
            MSR_PP0_POWER_LIMIT, MSR_PP0_ENERGY_STATUS,
            MSR_PP1_POWER_LIMIT, MSR_PP1_ENERGY_STATUS,
            MSR_DRAM_POWER_LIMIT, MSR_DRAM_ENERGY_STATUS,
            MSR_PLATFORM_POWER_LIMIT, MSR_PLATFORM_ENERGY_COUNTER]

    def __init__(self, cpuid, name, register_dicts):
        self.cpuid = cpuid
        self.name = name
        self.registers = {}
        # Later tables override any MSR configs in earlier tables
        for rdic in register_dicts:
            self.registers.update(rdic)

    @staticmethod
    def print_header():
        """Print header."""
        sys.stdout.write('Model' + CPU.DELIM + 'Name')
        for reg in CPU.REGS:
            sys.stdout.write(CPU.DELIM + reg)
        sys.stdout.write('\n')

    def print_line(self):
        """Print line fpr CPU."""
        sys.stdout.write(self.cpuid + CPU.DELIM  + self.name)
        for reg in CPU.REGS:
            sys.stdout.write(CPU.DELIM + self.registers.get(reg, 'None'))
        sys.stdout.write('\n')


if __name__ == "__main__":
    CPU.print_header()

    TBL_6 = {}
    TBL_7 = {}
    TBL_8 = {MSR_RAPL_POWER_UNIT: "Table 2-8",
             MSR_PKG_POWER_LIMIT: "Table 2-8",
             MSR_PKG_ENERGY_STATUS: PKG_DEFAULT,
             MSR_PP0_ENERGY_STATUS: PP0_DEFAULT}
    TBL_9 = {}
    TBL_10 = {MSR_RAPL_POWER_UNIT: "Table 2-10 (Same as 2-8)",
              MSR_PKG_POWER_LIMIT: PKG_DEFAULT}
    TBL_11 = {MSR_PP0_POWER_LIMIT: "Table 2-11"}
    ATOM_SILVERMONT = CPU("0x37", "ATOM_SILVERMONT", [TBL_6, TBL_7, TBL_8, TBL_9])
    ATOM_SILVERMONT.print_line()
    ATOM_SILVERMONT_MID = CPU("0x4A", "ATOM_SILVERMONT_MID", [TBL_6, TBL_7, TBL_8])
    ATOM_SILVERMONT_MID.print_line()
    ATOM_SILVERMONT_X = CPU("0x4D", "ATOM_SILVERMONT_X", [TBL_6, TBL_7, TBL_10])
    ATOM_SILVERMONT_X.print_line()
    ATOM_AIRMONT_MID = CPU("0x5A", "ATOM_AIRMONT_MID", [TBL_6, TBL_7, TBL_8])
    ATOM_AIRMONT_MID.print_line()
    ATOM_SOFIA = CPU("0x5D", "ATOM_SOFIA", [TBL_6, TBL_7, TBL_8])
    ATOM_SOFIA.print_line()
    ATOM_AIRMONT = CPU("0x4C", "ATOM_AIRMONT", [TBL_6, TBL_7, TBL_8, TBL_11])
    ATOM_AIRMONT.print_line()

    TBL_12 = {MSR_RAPL_POWER_UNIT: POWER_DEFAULT,
              MSR_PKG_POWER_LIMIT: PKG_DEFAULT,
              MSR_PKG_ENERGY_STATUS: PKG_DEFAULT,
              MSR_DRAM_POWER_LIMIT: DRAM_DEFAULT,
              MSR_DRAM_ENERGY_STATUS: DRAM_DEFAULT,
              MSR_PP0_ENERGY_STATUS: PP0_DEFAULT,
              MSR_PP1_ENERGY_STATUS: PP1_DEFAULT}
    TBL_13 = {}
    ATOM_GOLDMONT = CPU("0x5C", "ATOM_GOLDMONT", [TBL_6, TBL_12])
    ATOM_GOLDMONT.print_line()
    ATOM_GOLDMONT_X = CPU("0x5F", "ATOM_GOLDMONT_X", [])
    ATOM_GOLDMONT_X.print_line()
    ATOM_GOLDMONT_PLUS = CPU("0x7A", "ATOM_GOLDMONT_PLUS", [TBL_6, TBL_12, TBL_13])
    ATOM_GOLDMONT_PLUS.print_line()

    TBL_19 = {MSR_RAPL_POWER_UNIT: POWER_DEFAULT,
              MSR_PKG_POWER_LIMIT: PKG_DEFAULT,
              MSR_PKG_ENERGY_STATUS: PKG_DEFAULT,
              MSR_PP0_POWER_LIMIT: PP0_DEFAULT}
    TBL_20 = {MSR_PP0_ENERGY_STATUS: PP0_DEFAULT,
              MSR_PP1_POWER_LIMIT: PP1_DEFAULT,
              MSR_PP1_ENERGY_STATUS: PP1_DEFAULT}
    TBL_21 = {}
    TBL_22 = {MSR_DRAM_POWER_LIMIT: DRAM_DEFAULT,
              MSR_DRAM_ENERGY_STATUS: DRAM_DEFAULT,
              MSR_PP0_ENERGY_STATUS: PP0_DEFAULT}
    TBL_23 = {}
    SANDYBRIDGE = CPU("0x2A", "SANDYBRIDGE", [TBL_19, TBL_20, TBL_21])
    SANDYBRIDGE.print_line()
    SANDYBRIDGE_X = CPU("0x2D", "SANDYBRIDGE_X", [TBL_19, TBL_22, TBL_23])
    SANDYBRIDGE_X.print_line()

    TBL_24 = {MSR_PP0_ENERGY_STATUS: PP0_DEFAULT}
    TBL_25 = {MSR_DRAM_POWER_LIMIT: DRAM_DEFAULT,
              MSR_DRAM_ENERGY_STATUS: DRAM_DEFAULT,
              MSR_PP0_ENERGY_STATUS: PP0_DEFAULT}
    TBL_26 = {}
    TBL_27 = {}
    IVYBRIDGE = CPU("0x3A", "IVYBRIDGE", [TBL_19, TBL_20, TBL_21, TBL_24])
    IVYBRIDGE.print_line()
    IVYBRIDGE_X = CPU("0x3E", "IVYBRIDGE_X", [TBL_19, TBL_23, TBL_25, TBL_26, TBL_27])
    IVYBRIDGE_X.print_line()

    TBL_28 = {MSR_DRAM_ENERGY_STATUS: DRAM_DEFAULT}
    TBL_29 = {MSR_RAPL_POWER_UNIT: POWER_DEFAULT,
              MSR_PP0_ENERGY_STATUS: PP0_DEFAULT,
              MSR_PP1_POWER_LIMIT: PP1_DEFAULT,
              MSR_PP1_ENERGY_STATUS: PP1_DEFAULT}
    TBL_30 = {}
    TBL_31 = {MSR_RAPL_POWER_UNIT: POWER_DEFAULT,
              MSR_DRAM_POWER_LIMIT: DRAM_DEFAULT,
              MSR_DRAM_ENERGY_STATUS: DRAM_15_3,
              MSR_PP0_ENERGY_STATUS: RESERVED}
    TBL_32 = {}
    # TBL_24 specified at end of TBL_29
    HASWELL_CORE = CPU("0x3C", "HASWELL_CORE", [TBL_19, TBL_20, TBL_21, TBL_24, TBL_28, TBL_29])
    HASWELL_CORE.print_line()
    HASWELL_X = CPU("0x3F", "HASWELL_X", [TBL_19, TBL_28, TBL_31, TBL_32])
    HASWELL_X.print_line()
    # TBL_21 specified at end of TBL_30
    HASWELL_ULT = CPU("0x45", "HASWELL_ULT", [TBL_19, TBL_20, TBL_21, TBL_28, TBL_29, TBL_30])
    HASWELL_ULT.print_line()
    # TBL_24 specified at end of TBL_29
    HASWELL_GT3E = CPU("0x46", "HASWELL_GT3E", [TBL_19, TBL_20, TBL_21, TBL_24, TBL_28, TBL_29])
    HASWELL_GT3E.print_line()

    TBL_33 = {}
    TBL_34 = {MSR_PP0_ENERGY_STATUS: PP0_DEFAULT}
    TBL_35 = {MSR_RAPL_POWER_UNIT: POWER_DEFAULT,
              MSR_DRAM_POWER_LIMIT: DRAM_DEFAULT,
              MSR_DRAM_ENERGY_STATUS: DRAM_15_3,
              MSR_PP0_ENERGY_STATUS: RESERVED}
    TBL_36 = {}
    TBL_37 = {}
    BROADWELL_CORE = CPU("0x3D", "BROADWELL_CORE", [TBL_19, TBL_20, TBL_21, TBL_24, TBL_28, TBL_29, TBL_33, TBL_34])
    BROADWELL_CORE.print_line()
    BROADWELL_GT3E = CPU("0x47", "BROADWELL_GT3E", [TBL_19, TBL_20, TBL_21, TBL_24, TBL_28, TBL_29, TBL_33, TBL_34])
    BROADWELL_GT3E.print_line()
    # BROADWELL_X: Section 2.5.12 specifies the prior tables for this architecture.
    # TODO: Also TBL_36? Mentioned at start of Section 2.5.12, but not included in explicit list
    # TODO: Comment at end of TBL_37 is for 0x45? Won't use (no effect on results anyway)...
    BROADWELL_X = CPU("0x4F", "BROADWELL_X", [TBL_19, TBL_20, TBL_28, TBL_33, TBL_35, TBL_37])
    BROADWELL_X.print_line()
    # BROADWELL_XEON_D: See 2.15.1 for mention of Tables 19 and 28
    BROADWELL_XEON_D = CPU("0x56", "BROADWELL_XEON_D", [TBL_19, TBL_28, TBL_33, TBL_35, TBL_36])
    BROADWELL_XEON_D.print_line()

    TBL_38 = {MSR_PP0_ENERGY_STATUS: PP0_DEFAULT,
              MSR_PLATFORM_ENERGY_COUNTER: PLATFORM_DEFAULT,
              MSR_PLATFORM_POWER_LIMIT: PLATFORM_DEFAULT}
    TBL_39 = {}
    TBL_40 = {}
    TBL_41 = {}
    TBL_42 = {MSR_RAPL_POWER_UNIT: POWER_DEFAULT,
              MSR_DRAM_POWER_LIMIT: DRAM_DEFAULT,
              MSR_DRAM_ENERGY_STATUS: DRAM_15_3,
              MSR_PP0_ENERGY_STATUS: RESERVED}
    SKYLAKE_MOBILE = CPU("0x4E", "SKYLAKE_MOBILE", [TBL_19, TBL_20, TBL_24, TBL_28, TBL_34, TBL_38, TBL_39])
    SKYLAKE_MOBILE.print_line()
    # Top of Section 2.16 says TBL_39 (Uncore) is used for 0x55, but TBL_39 doesn't mention it
    SKYLAKE_X = CPU("0x55", "SKYLAKE_X", [TBL_19, TBL_20, TBL_24, TBL_28, TBL_34, TBL_38, TBL_42])
    SKYLAKE_X.print_line()
    SKYLAKE_DESKTOP = CPU("0x5E", "SKYLAKE_DESKTOP", [TBL_19, TBL_20, TBL_24, TBL_28, TBL_34, TBL_38, TBL_39])
    SKYLAKE_DESKTOP.print_line()
    KABYLAKE_MOBILE = CPU("0x8E", "KABYLAKE_MOBILE", [TBL_19, TBL_20, TBL_24, TBL_28, TBL_34, TBL_38, TBL_39, TBL_40])
    KABYLAKE_MOBILE.print_line()
    KABYLAKE_DESKTOP = CPU("0x9E", "KABYLAKE_DESKTOP", [TBL_19, TBL_20, TBL_24, TBL_28, TBL_34, TBL_38, TBL_39, TBL_40])
    KABYLAKE_DESKTOP.print_line()
    CANNONLAKE_MOBILE = CPU("0x66", "CANNONLAKE_MOBILE", [TBL_19, TBL_20, TBL_24, TBL_28, TBL_34, TBL_38, TBL_39, TBL_41])
    CANNONLAKE_MOBILE.print_line()

    TBL_43 = {MSR_RAPL_POWER_UNIT: POWER_DEFAULT,
              MSR_PKG_POWER_LIMIT: PKG_DEFAULT,
              MSR_PKG_ENERGY_STATUS: PKG_DEFAULT,
              MSR_DRAM_POWER_LIMIT: DRAM_DEFAULT,
              MSR_DRAM_ENERGY_STATUS: DRAM_DEFAULT,
              MSR_PP0_POWER_LIMIT: PP0_DEFAULT,
              MSR_PP0_ENERGY_STATUS: PP0_DEFAULT}
    TBL_44 = {}
    XEON_PHI_KNL = CPU("0x57", "XEON_PHI_KNL", [TBL_43])
    XEON_PHI_KNL.print_line()
    XEON_PHI_KNM = CPU("0x85", "XEON_PHI_KNM", [TBL_43, TBL_44])
    XEON_PHI_KNM.print_line()

    # Last updated for Software Developer's Manual, Volume 4 - May 2018
