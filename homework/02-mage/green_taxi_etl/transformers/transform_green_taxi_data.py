if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
@transformer
def transform(data, *args, **kwargs):
    # Remove rows where the passenger count is equal to 0 or the trip distance is equal to zero.
    data = data[~((data['passenger_count'] == 0) | (data['trip_distance'] == 0))]

    # Create a new column lpep_pickup_date by converting lpep_pickup_datetime to a date.
    data["lpep_pickup_date"] = data["lpep_pickup_datetime"].dt.date

    # Rename columns in Camel Case to Snake Case, e.g. VendorID to vendor_id.
    # solution from https://stackoverflow.com/questions/74643621/convert-dataframe-column-names-from-camel-case-to-snake-case
    data.columns = (
        data.columns
        .str.replace('(?<=[a-z])(?=[A-Z])', '_', regex=True)
        .str.lower()
    )
    
    print()
    print(data["vendor_id"].unique())
    print()

    return data


@test
def test_passenger_count_non_zero(output, *args) -> None:
    assert  output["passenger_count"].le(0).sum() == 0, "Found rows with passenger_count = 0"

@test
def test_trip_distance_non_zero(output, *args) -> None:
    assert  output["trip_distance"].le(0).sum() == 0, "Found rows with trip_distance = 0"
    
@test
def test_vendor_id_in_columns(output, *args) -> None:
    assert "vendor_id" in output.columns, "vendor_id not in columns"
