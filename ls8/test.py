obj = {
  "cat": "bob",
  "dog": 23,
  19: 18,
  90: "fish"
}

count = 0

for key in obj:
    if type(obj[key]) == int:
        count += obj[key]

print(count)