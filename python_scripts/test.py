logger.info('Python Test Script Running')

entity_ids  = data.get('entity_ids')

logger.info("entity_ids %s", entity_ids)

sun = hass.states.get('sun.sun')

logger.info("sun %s", sun.attributes.get("elevation"))