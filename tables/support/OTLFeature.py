from lxml.etree import Element
from data import tag


# OTLFeature
# -----------------------------
# Classes representing common OpenType Layout Feature structures.
# (https://docs.microsoft.com/en-us/typography/opentype/spec/chapter2#features-and-lookups)



class Feature:
    """
    Class representing a placeholder Feature table.
    Intended to have the right data for TTX GSUB generation.
    """
    def __init__(self):
        self.whatever = 0

    def toTTX(self):
        feature = Element("Feature")
        feature.append(Element("LookupListIndex", {"index": "0", "value": "0"}))

        return feature

class FeatureRecord:
    """
    Class representing a placeholder FeatureRecord table.
    Intended to have the right data for TTX GSUB generation.
    """
    def __init__(self):
        self.tag = tag("liga")
        self.feature = Feature() # placeholder feature

    def toTTX(self, index):
        featureRecord = Element("FeatureRecord", {"index": str(index) })
        featureRecord.append(Element("FeatureTag", {"value": str(self.tag) }))
        featureRecord.append(self.feature.toTTX())

        return featureRecord


class FeatureList:
    """
    Class representing a FeatureList table.
    """
    def __init__(self):
        self.featureRecords = [FeatureRecord()]

    def toTTX(self):
        featureList = Element("FeatureList")

        for index, fr in enumerate(self.featureRecords):
            featureList.append(fr.toTTX(index))

        return featureList
