
# Usage
#   action:
#    - service: python_script.fade_in
#      data_template:
#        entity_id: light.kitchen
#        ideal_start_angle_of_sun: -4
#        current_angle_of_sun: {{ states.sun.sun.attributes.azimuth }}
#        time_of_sunset: {{ as_timestamp(states.sun.sun.attributes.next_setting) }}
#        time_now: {{ as_timestamp(now()) }}
#        end_level_pct: 100
#        step_in_level_pct: 2
#        start_level_pct: 0
#



entity_id  = data.get('entity_id')
ideal_start_angle_of_sun = int(data.get('ideal_start_angle_of_sun'))
current_angle_of_sun = float(data.get('current_angle_of_sun'))
time_of_sunset = float(data.get('time_of_sunset'))
time_now = float(data.get('time_now'))
end_level_pct = int(data.get('end_level_pct'))
step_pct  = int(data.get('step_in_level_pct'))
start_level_pct = int(data.get('start_level_pct'))


# find precent of sunset complete
absolute_degrees_of_total_sunset = abs(ideal_start_angle_of_sun)
absolute_degrees_of_sunset_thus_far = abs(ideal_start_angle_of_sun - current_angle_of_sun)
percent_of_sunset_complete = absolute_degrees_of_sunset_thus_far / absolute_degrees_of_total_sunset

# find time until the sunets
time_till_sunset = time_of_sunset - time_now + 120

# Adjest the light level to start based on how mush sunset has already passed
adjusted_start_level_pct = ((end_level_pct - start_level_pct) * percent_of_sunset_complete) + start_level_pct

# How much to wait between each increase of ligts
sleep_delay = time_till_sunset / step_pct

start_level = int(255*adjusted_start_level_pct/100)
end_level = int(255*end_level_pct/100)
step = int(255*step_pct/100)

new_level = start_level
while new_level < end_level :
	states = hass.states.get(entity_id)
	current_level = states.attributes.get('brightness') or 0
	if (current_level > new_level) :
		logger.debug('Exiting Fade In')
		break;
	else :
		logger.debug('Setting brightness of ' + str(entity_id) + ' from ' + str(current_level) + ' to ' + str(new_level))
		data = { "entity_id" : entity_id, "brightness" : new_level }
		hass.services.call('light', 'turn_on', data)
		new_level = new_level + step
		time.sleep(sleep_delay)