from PIL import Image, ImageOps
def split_bytes_to_rows(byte_string, num_cols=320):
  """
  Splits a long byte string into rows with a specified number of columns.

  Args:
    byte_string: The byte string to split.
    num_cols: The number of columns per row (default: 320).

  Returns:
    A list of byte arrays, where each element represents a row.
  """
  if not isinstance(byte_string, bytes):
    raise TypeError("Input must be a byte string")

  # Calculate the number of rows
  num_rows = (len(byte_string) + num_cols - 1) // num_cols

  # Split the byte string into rows using list comprehension
  rows = [byte_string[i * num_cols: (i + 1) * num_cols] for i in range(num_rows)]

  return rows
def parse(path):
    width, height = 320, 240
    img = Image.new("L", (width, height))
  
    data = open(path, "rb").read()
    data = split_bytes_to_rows(data)
  
    for y in range(height):
      for x in range(width):
        img.putpixel((x, y), data[y][x])

    try:
      img = ImageOps.grayscale(img)
      img.save(f"{path.split('.')[0]}.png")
    except Exception as e:
      print("Error:",e,path)
  
limit = 2 
for x in range(limit):
    parse(f"image_{x}.bin")
