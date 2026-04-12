import math
from functools import total_ordering


@total_ordering
class Circle:
	def __init__(self, radius: float) -> None:
		if radius < 0:
			raise ValueError("Radius must be non-negative")
		self._radius = float(radius)

	@classmethod
	def from_diameter(cls, diameter: float) -> "Circle":
		if diameter < 0:
			raise ValueError("Diameter must be non-negative")
		return cls(diameter / 2)

	@property
	def radius(self) -> float:
		return self._radius

	@radius.setter
	def radius(self, value: float) -> None:
		if value < 0:
			raise ValueError("Radius must be non-negative")
		self._radius = float(value)

	@property
	def diameter(self) -> float:
		return self._radius * 2

	@diameter.setter
	def diameter(self, value: float) -> None:
		if value < 0:
			raise ValueError("Diameter must be non-negative")
		self._radius = float(value) / 2

	def area(self) -> float:
		return math.pi * (self._radius ** 2)

	def __repr__(self) -> str:
		return f"Circle(radius={self.radius:.2f}, diameter={self.diameter:.2f})"

	def __add__(self, other: "Circle") -> "Circle":
		if not isinstance(other, Circle):
			return NotImplemented
		return Circle(self.radius + other.radius)

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, Circle):
			return NotImplemented
		return math.isclose(self.radius, other.radius)

	def __lt__(self, other: "Circle") -> bool:
		if not isinstance(other, Circle):
			return NotImplemented
		return self.radius < other.radius


if __name__ == "__main__":
	c1 = Circle(5)
	c2 = Circle.from_diameter(8)
	c3 = Circle(3)

	print("Initial circles:")
	print(c1)
	print(c2)
	print(c3)

	print("\nArea values:")
	print(f"c1 area = {c1.area():.2f}")
	print(f"c2 area = {c2.area():.2f}")
	print(f"c3 area = {c3.area():.2f}")

	print("\nAddition:")
	print(f"c1 + c2 = {c1 + c2}")

	print("\nComparisons:")
	print(f"c1 > c2 ? {c1 > c2}")
	print(f"c1 == c2 ? {c1 == c2}")
	print(f"c2 == Circle(4) ? {c2 == Circle(4)}")

	circles = [c1, c2, c3, Circle.from_diameter(14), Circle(1.5)]
	circles.sort()

	print("\nSorted circles:")
	for circle in circles:
		print(circle)
