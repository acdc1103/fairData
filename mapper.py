def map_to_unified_schema(fdic={}, world_bank={}):
    print(f"FDIC: {fdic}")
    print(f"WORLD BANK: {world_bank}")
    unified_schema = {
        "identifier": fdic.get("identifier", world_bank.get("id")),
        "title": fdic.get("title", world_bank.get("name")),
        "description": fdic.get("description", world_bank.get("description")),
        "publisher": fdic.get("publisher", world_bank.get("attribution")),
        "accessLevel": fdic.get("accessLevel", world_bank.get('approvals')[0]['targetAudience'] if world_bank.get('approvals') else None),
        "keyword": fdic.get("keyword", world_bank.get("keyword", [])),
        "dataUri": world_bank.get("dataUri", fdic.get('distribution')[0]['downloadURL'] if fdic.get('distribution') else None),
        "license": fdic.get("license",world_bank.get("license")),
        "metadataUpdatedAt": fdic.get("metadataUpdatedAt",world_bank.get("metadataUpdatedAt", "")),
        "createdAt": fdic.get("createdAt",world_bank.get("createdAt")),
        "webUri": world_bank.get("webUri", fdic.get('distribution')[0]['downloadURL'] if fdic.get('distribution') else None),
    }
    return unified_schema