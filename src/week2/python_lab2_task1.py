"""
Lab 3.1 – Simple Datasets and Aggregates

Goals:
- Create and manipulate Python lists and dictionaries.
- Compute aggregates such as sum, average, max, and min.

Instructions:
1. Create a list `temperatures` with daily temperatures for one week.
2. Create a dictionary `city_population` with at least 5 cities and their populations.
3. Compute:
   - The average temperature.
      - The maximum and minimum population.
         - The total population of all cities.
         4. Print your results in a clear, formatted way.
"""

temperatures = [12, 15, 14, 18, 20, 17, 13]
city_population = {
    "Riga": 605802,
    "Daugavpils": 78389,
    "Liepaja": 66340,
    "Jelgava": 54693,
    "Jurmala": 50001,
}

average_temperature = sum(temperatures) / len(temperatures)
largest_city = max(city_population, key=city_population.get)
largest_population = max(city_population.values())
total_population = sum(city_population.values())

print("Average temperature:", average_temperature)
print("Largest city:", largest_city, "-", largest_population)
print("Total population:", total_population)
