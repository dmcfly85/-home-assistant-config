# Usage
# - alias: "Start fading lights as sunsets"
#   trigger:
#     platform: numeric_state
#     entity_id: sun.sun
#     value_template: "{{ state.attributes.elevation }}"
#     below: 4.0
#   action:
#     service: python_script.fade_up_against_sunset
#     data_template:
#       entity_id: group.all_lights
#       ideal_start_angle_of_sun: 4
#       current_angle_of_sun: "{{ states.sun.sun.attributes.elevation }}"
#       time_of_sunset: "{{ as_timestamp(states.sun.sun.attributes.next_setting) }}"
#       end_level_pct: 100
#       start_level_pct: 0
#       step_in_level_pct: 2
#       time_now: "{{ as_timestamp(now()) }}"

entity_id  = data.get('entity_id')
ideal_start_angle_of_sun = float(data.get('ideal_start_angle_of_sun'))
current_angle_of_sun = float(data.get('current_angle_of_sun'))
time_of_sunset = float(data.get('time_of_sunset'))
time_now = float(data.get('time_now'))
end_level_pct = int(data.get('end_level_pct'))
step_pct  = int(data.get('step_in_level_pct'))
start_level_pct = int(data.get('start_level_pct'))

allow_loop_switch = hass.states.get('allow_pre_sunset_script').state

logger.info(switch.state)

logger.info("""Starting fade_up_against_sunset with
entity_id: %s
ideal_start_angle_of_sun: %f
current_angle_of_sun: %f
time_of_sunset: %f
time_now: %f
end_level_pct: %i
start_level_pct: %i
step_pct: %i
allow_loop_switch: %s
""" % (entity_id, ideal_start_angle_of_sun, current_angle_of_sun, time_of_sunset, time_now, end_level_pct, start_level_pct, step_pct, switch ) )



# find precent of sunset complete
absolute_degrees_of_total_sunset = abs(ideal_start_angle_of_sun)
absolute_degrees_of_sunset_thus_far = abs(ideal_start_angle_of_sun - current_angle_of_sun)
percent_of_sunset_complete = absolute_degrees_of_sunset_thus_far / absolute_degrees_of_total_sunset

# find time until the sunets
time_till_sunset = time_of_sunset - time_now

# Adjest the light level to start based on how mush sunset has already passed
adjusted_start_level_pct = ((end_level_pct - start_level_pct) * percent_of_sunset_complete) + start_level_pct

# How much to wait between each increase of ligts
sleep_delay = (time_till_sunset / (end_level_pct - adjusted_start_level_pct ) * step_pct )

start_level = int(255*adjusted_start_level_pct/100)
end_level = int(255*end_level_pct/100)
step = int(255*step_pct/100)

logger.info("""Starting fade_up_against_sunset
absolute_degrees_of_total_sunset: %f
absolute_degrees_of_sunset_thus_far: %f
percent_of_sunset_complete: %f
time_till_sunset: %f
adjusted_start_level_pct: %f
step: %i
sleep_delay: %f
""" % (absolute_degrees_of_total_sunset, absolute_degrees_of_sunset_thus_far, percent_of_sunset_complete, time_till_sunset, adjusted_start_level_pct, step, sleep_delay ) )


new_level = start_level
while new_level < end_level and allow_loop_switch == 'off' :
	states = hass.states.get(entity_id)
	current_level = states.attributes.get('brightness') or 0
	allow_loop_switch = hass.states.get('input_boolean.allow_pre_sunset_script').state
	if (current_level > new_level) :
		logger.info('Exiting Fade In')
		break;
	else :
		logger.info('Allow Loop Switch: ' + str(allow_loop_switch) + ' Setting brightness of ' + str(entity_id) + ' from ' + str(current_level) + ' to ' + str(new_level))
		data = { "entity_id" : entity_id, "brightness" : new_level }
		hass.services.call('light', 'turn_on', data)
		new_level = new_level + step
		time.sleep(sleep_delay)
		
logger.info('Script ended')
		
		