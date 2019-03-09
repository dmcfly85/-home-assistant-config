logger.warn('Python Test Script Running')

entity_ids  = data.get('entity_ids')

logger.info("entity_ids %s", entity_ids)

sun = hass.states.get('sun.sun')

logger.info("sun %s", sun.attributes.get("elevation"))

switch = hass.states.get('input_boolean.sunset_fade_bailer').state

logger.info(switch)

a = 1

if switch == 'on' and a == 1:
  logger.info('in if')
  
  
for entity in entity_ids:
   e = hass.states.get(entity).attributes.get("brightness")
   logger.info(e)