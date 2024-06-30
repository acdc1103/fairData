from logger import logger

def map_to_unified_schema(data_gov={}, world_bank={}):
    """Maps metadata from Data.gov and World Bank to a unified schema.

    Args:
        data_gov (dict, optional): Data Gov Metadata. Defaults to {}.
        world_bank (dict, optional): World Bank Metadata. Defaults to {}.

    Returns:
        dict: Mapped Metadata
    """

    # Logging the mapping process
    logger.info("Mapping Metadata")
    logger.debug(f"Data Gov Metadata: {data_gov}")
    logger.debug(f"World Bank Metadata: {world_bank}")
    
    # Mapping the metadata to a unified schema
    # If further databases are added this mapping has to be enhanced respectively
    unified_schema = {
        "identifier": data_gov.get("identifier", 
                                world_bank.get("id")),

        "title": data_gov.get("title", 
                                world_bank.get("name")),

        "description": data_gov.get("description",
                                world_bank.get("description")),

        "publisher": data_gov.get("publisher", 
                                world_bank.get("attribution")),

        "accessLevel": data_gov.get("accessLevel", 
                                world_bank.get("approvals")[0]["targetAudience"] if world_bank.get("approvals") else None),

        "keyword": data_gov.get("keyword", 
                                world_bank.get("keyword", [])),

        "dataUri": world_bank.get("dataUri", 
                                data_gov.get("distribution")[0]["downloadURL"] if data_gov.get("distribution") else None),

        "license": data_gov.get("license",world_bank.get("license")),

        "metadataUpdatedAt": data_gov.get("metadataUpdatedAt",
                                        world_bank.get("metadataUpdatedAt", "")),

        "createdAt": data_gov.get("createdAt",
                                world_bank.get("createdAt")),

        "webUri": world_bank.get("webUri", 
                                data_gov.get("distribution")[0]["downloadURL"] if data_gov.get("distribution") else None),
    }

    logger.debug(f"Unified Schema: {unified_schema}")

    return unified_schema