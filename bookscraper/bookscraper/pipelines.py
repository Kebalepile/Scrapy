# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # Strip all whitespace from strings.
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != "description":
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()

        # Category & Product Type ----> switch to lowercase
        lowercase_keys = ["category", "product_type"]
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        # Price ---> convert to float
        price_keys = ["price", "price_excl_tax", "price_inc_tax", "tax"]
        for price_key in price_keys:
            value = adapter.get(price_key)
            
            print(value)
            adapter[price_key] = float(value[1:])

        # Availability ----> extract number of books in stock.
        availability_string = adapter.get("availability")
        split_string_array = availability_string.split("(")
        if (len(split_string_array)) < 2:
            adapter["availability"] = 0
        else:
            availability_array = split_string_array[1].split(" ")
            adapter["availability"] = int(availability_array[0])

        # Reviews -----> conver to interger.
        num_reviews = adapter.get("num_reviews")
        adapter["num_reviews"] = int(num_reviews)

        # Starts rating ---> convert to interger.
        stars_string = adapter.get("stars")
        split_stars_array = stars_string.split(" ")
        start_rating = split_stars_array[1].lower()

        stars_conversion = {
            "zero": 0,
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5
        }
        adapter["stars"] = stars_conversion[start_rating]

        return item
