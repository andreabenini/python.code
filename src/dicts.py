
# Iterating over a dict() with keys in order to delete elements from it
Clients = {}
# insert elements here...
# now loop to delete them (need to use a list, iterator goes in panic when I delete items from there)
for Key in list(Clients.keys()):
    logger.debug("Item=%s" % (Key))
    if NeedToDelete(Key):
        logger.debug("Remove()")
        del Clients[Key]
logger.warning("done all")
