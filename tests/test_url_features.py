from phishdetector.feature_extraction.extractor import (
    PhishingFeatureExtractor
)


extractor = PhishingFeatureExtractor()

url = "https://example.com"

features = extractor.extract(url)

print("\nURL:")
print(url)

print("\nNumber of features:")
print(len(features))

print("\nFeatures:")

for name, value in features.items():
    print(f"{name}: {value}")