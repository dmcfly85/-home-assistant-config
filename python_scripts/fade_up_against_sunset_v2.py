
#   action:
#     service: python_script.fade_up_against_sunset
#     data_template:
#       entity_ids: 
#         - light.kitchen
#         - light.dining_room
#       start_angle_of_sun: 4
#       end_angle_of_sun: -1
#       start_level_pct: 0
#       end_level_pct: 100
#       step_pct: 2
#       ignore_start_level_for_lights_already_on: true
#       trigger_script_when_done:
#       allow_fade_boolean_name: 
#       run_script_with_id: 

current_angle_of_sun = float(hass.states.get('sun.sun').attributes.get("elevation"))

entity_ids = data.get('entity_ids')
start_angle_of_sun = float(data.get('start_angle_of_sun') or current_angle_of_sun) 
end_angle_of_sun = float(data.get('end_angle_of_sun')  or 0)
end_level_pct = int(data.get('end_level_pct') or 100) 
start_level_pct = int(data.get('start_level_pct')) or 0
step_pct = int(data.get('step_pct') or 2)
ignore_start_level_for_lights_already_on = data.get('ignore_start_level_for_lights_already_on') or False
trigger_script_when_done = data.get('trigger_script_when_done')
allow_fade_boolean_name = data.get('allow_fade_boolean_name')
run_script_with_id = data.get('run_script_with_id')

allow_fade_boolean_state = hass.states.get(allow_fade_boolean_name).state or 'on'

time_of_sunset = datetime.datetime.strptime(hass.states.get('sun.sun').attributes.get("next_setting")[:19], '%Y-%m-%dT%H:%M:%S').timestamp()
time_now = datetime.datetime.now().timestamp()
total_degress_of_sunset = abs(start_angle_of_sun - end_angle_of_sun )
degrees_of_sunset_thus_far = abs(start_angle_of_sun - current_angle_of_sun)
percent_of_sunset_complete = degrees_of_sunset_thus_far / total_degress_of_sunset
time_till_sunset = time_of_sunset - time_now

# # Adjest the light level to start based on how mush sunset has already passed
adjusted_start_level_pct = ((end_level_pct - start_level_pct) * percent_of_sunset_complete) + start_level_pct

# # How much to wait between each increase of ligts
sleep_delay = (time_till_sunset / (end_level_pct - adjusted_start_level_pct ) * step_pct )

start_level = int(255*adjusted_start_level_pct/100)
end_level = int(255*end_level_pct/100)
step = int(255*step_pct/100)


logger.info("""
Starting: %s
entity_ids: %s
current_angle_of_sun: %f
start_angle_of_sun: %f
end_angle_of_sun: %f
start_level_pct: %i
end_level_pct: %i
ignore_start_level_for_lights_already_on: %s
trigger_script_when_done: %s
allow_fade_boolean_name: %s
allow_fade_boolean_state: %s
""" % (
       run_script_with_id,
       entity_ids,
       current_angle_of_sun, 
       start_angle_of_sun, 
       end_angle_of_sun, 
       start_level_pct, 
       end_level_pct, 
       ignore_start_level_for_lights_already_on, 
       trigger_script_when_done, 
       allow_fade_boolean_name,
       allow_fade_boolean_state
      ))
      
logger.debug("""
Varibles for: %s
time_of_sunset: %f
time_now: %f
total_degress_of_sunset: %f
degrees_of_sunset_thus_far: %f
percent_of_sunset_complete: %f
time_till_sunset: %f
adjusted_start_level_pct %f
sleep_delay: %f
start_level: %f
end_level: %f
step: %f

""" % (
    run_script_with_id,
    time_of_sunset,
    time_now,
    total_degress_of_sunset,
    degrees_of_sunset_thus_far,
    percent_of_sunset_complete,
    time_till_sunset,
    adjusted_start_level_pct,
    sleep_delay,
    start_level,
    end_level,
    step
    ))


new_level = start_level
highest_level = 0

while new_level < end_level and allow_fade_boolean_state == 'on' :
  for entity_id in entity_ids:
	state = hass.states.get(entity_id)
	current_level = states.attributes.get('brightness') or 0
	
	if (current_level < new_level)
        #highest_level = current_level if current_level > higest_level else highest_level
        data = { "entity_id" : entity_id, "brightness" : new_level }
        hass.services.call('light', 'turn_on', data)
        logger.info('Allow Loop Switch: ' + str(allow_loop_switch) + ' Setting brightness of ' + str(entity_id) + ' from ' + str(current_level) + ' to ' + str(new_level))

  
  new_level = new_level + step
  allow_loop_switch = hass.states.get('input_boolean.allow_pre_sunset_script').state
  time.sleep(sleep_delay)
# 	if (current_level > new_level) :
# 		logger.info('Exiting Fade In')
# 		break;
# 	else :
# 		
# 		data = { "entity_id" : entity_id, "brightness" : new_level }
# 		hass.services.call('light', 'turn_on', data)
# 		new_level = new_level + step
# 		time.sleep(sleep_delay)
		
# logger.info('Script ended')
		
		