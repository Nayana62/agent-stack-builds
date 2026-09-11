SAMPLE_FUNCTIONS = {
    "clean": '''
def calculate_average(numbers: list[float]) -> float:
    """Return the arithmetic mean of a non-empty list of numbers."""
    if not numbers:
        raise ValueError("numbers must not be empty")
    return sum(numbers) / len(numbers)
''',
    "has issues": """
def getUserAge(users, user_id, cache={}):
    if user_id in cache:
        return cache[user_id]
    for user in users:
        if user["id"] == user_id:
            age = 2026 - user["birth_year"]
            cache[user_id] = age
            return age
""",
    "messy": """
def process(d,x=None):
  try:
    r=[]
    for i in range(len(d)):
      if d[i]!=None and d[i]>0: r.append(d[i]*1.18)
      elif x: r.append(x)
    return r
  except:
    pass
""",
}
