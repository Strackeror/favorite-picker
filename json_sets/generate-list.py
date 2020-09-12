import json
import sys

template = """
(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        define([], factory);
    } else if (typeof module === 'object' && module.exports) {
        module.exports = factory();
    } else {
        root.item_list = factory();
    }
}(typeof self !== 'undefined' ? self : this, function () {
    return $JSON$
}));
"""

# url for json sets : http://dd.b.pvp.net/latest/setX/en_us/data/setX-en_us.json

set_array = []
for path in sys.argv[1:]:
    f = open(path, encoding='utf-8')
    set_array += json.load(f)

output_array = []
for card in set_array:
    if card["rarity"] == "None" and card["supertype"] == "Champion":
        continue
    obj = {}
    obj["id"] = card["cardCode"]
    obj["name"] = card["name"]
    obj["image"] = card["assets"][0]["gameAbsolutePath"]
    obj["rarity"] = card["rarity"].lower()
    if not card["collectible"]:
        print(card["name"], card["rarity"], file=sys.stderr)
        obj["rarity"] = "none"

    obj["region"] = card["regionRef"]
    obj["type"] = card["type"]
    output_array.append(obj)
print(template.replace("$JSON$", json.dumps(output_array, indent=True)))

