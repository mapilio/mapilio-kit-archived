import typing as T

import jsonschema

from mapilio_kit import types_fmt


def feature_collection_schema(features: dict) -> dict:
    return {
        "type": "object",
        "properties": {
            "type": {"type": "string", "enum": "FeatureCollection"},
            "features": {
                "type": "array",
                "items": features,
            },
        },
    }


def feature_schema(geometry: dict, properties: T.Any) -> dict:
    return {
        "type": "object",
        "properties": {
            "type": {"type": "string", "enum": "Feature"},
            "properties": properties,
            "geometry_schema": geometry,
        },
    }


def position_schema():
    return {
        "type": "array",
        "items": {
            "type": "number",
        },
    }


def point_schema():
    return {
        "type": "object",
        "properties": {
            "type": {"type": "string"},
            "coordinates": position_schema(),
        },
    }


def single_feature_to_desc(
    feature: dict, quiet=False
) -> T.Optional[types.FinalImageDescriptionFromGeoJSON]:
    input_schema = feature_schema(point_schema(), {})
    if quiet:
        try:
            jsonschema.validate(instance=feature, schema=input_schema)
        except jsonschema.exceptions.ValidationError:
            return None
    lng, lat = feature["geometry"]["coordinates"]
    desc = {
        "Latitude": lng,
        "Longitude": lat,
        **feature["properties"],
    }
    return T.cast(types.FinalImageDescriptionFromGeoJSON, desc)


def feature_collection_to_desc(
    feature_collection: dict,
) -> T.List[types.FinalImageDescriptionFromGeoJSON]:
    input_schema = feature_collection_schema(
        feature_schema(
            point_schema(),
            True,
        )
    )
    jsonschema.validate(instance=feature_collection, schema=input_schema)
    desc = [
        single_feature_to_desc(f, quiet=True) for f in feature_collection["features"]
    ]
    return [d for d in desc if d is not None]


def single_desc_to_feature(
    desc: types.FinalImageDescription, quiet=False
) -> T.Optional[dict]:
    input_schema = {
        "type": "array",
        "items": types.FinalImageDescriptionSchema,
    }
    if quiet:
        try:
            jsonschema.validate(instance=desc, schema=input_schema)
        except jsonschema.exceptions.ValidationError:
            return None
    properties = {**desc}
    del properties["Longitude"]
    del properties["Latitude"]
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [desc["Longitude"], desc["Latitude"]],
        },
        "properties": properties,
    }


def desc_to_feature_collection(desc: T.List[types.FinalImageDescription]) -> dict:
    features = [single_desc_to_feature(d) for d in desc]
    return {
        "type": "FeatureCollection",
        "features": features,
    }


if __name__ == "__main__":
    import json
    import sys

    with open(sys.argv[1]) as fp:
        descs = json.load(fp)
        descs = [d for d in descs if "error" not in d]
        feature_collection = desc_to_feature_collection(descs)
        print(json.dumps(feature_collection, indent=4))

    with open("schema/image_description_schema.geojson", "w") as outfile:
        outfile.write(json.dumps(feature_collection, indent=4))
