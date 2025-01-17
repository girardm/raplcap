/**
 * Functionality specific to raplcap-msr.
 * Units generally indicate the precision at which relevant values can be read or written.
 *
 * @author Connor Imes
 * @date 2018-05-19
 */
#ifndef _RAPLCAP_MSR_H_
#define _RAPLCAP_MSR_H_

#ifdef __cplusplus
extern "C" {
#endif

#include <raplcap.h>

/**
 * Get the time units for a zone in seconds.
 *
 * @param rc
 * @param socket
 * @param zone
 * @return Seconds on success, a negative value on error
 */
double raplcap_msr_get_time_units(const raplcap* rc, uint32_t socket, raplcap_zone zone);

/**
 * Get the power units for a zone in Watts.
 *
 * @param rc
 * @param socket
 * @param zone
 * @return Watts on success, a negative value on error
 */
double raplcap_msr_get_power_units(const raplcap* rc, uint32_t socket, raplcap_zone zone);

/**
 * Get the energy units for a zone in Joules.
 *
 * @param rc
 * @param socket
 * @param zone
 * @return Joules on success, a negative value on error
 */
double raplcap_msr_get_energy_units(const raplcap* rc, uint32_t socket, raplcap_zone zone);

#ifdef __cplusplus
}
#endif

#endif
