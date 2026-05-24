import math
import random
import matplotlib.pyplot as plt
import os


class Node:
    def __init__(self, point, left=None, right=None):
        self.point = point
        self.left = left
        self.right = right


def build_kdtree(points, depth=0):
    if not points:
        return None

    axis = depth % 2

    points.sort(key=lambda p: p[axis])
    median = len(points) // 2

    return Node(
        point=points[median],
        left=build_kdtree(points[:median], depth + 1),
        right=build_kdtree(points[median + 1:], depth + 1)
    )


def search_circle(node, center, radius, depth=0, result=None):
    if result is None:
        result = []

    if node is None:
        return result

    dx = node.point[0] - center[0]
    dy = node.point[1] - center[1]

    if dx * dx + dy * dy <= radius * radius:
        result.append(node.point)

    axis = depth % 2

    if center[axis] < node.point[axis]:
        good_side = node.left
        bad_side = node.right
    else:
        good_side = node.right
        bad_side = node.left

    search_circle(good_side, center, radius, depth + 1, result)

    if abs(center[axis] - node.point[axis]) <= radius:
        search_circle(bad_side, center, radius, depth + 1, result)

    return result


def visualize(points, found_points, center, radius):
    fig, ax = plt.subplots(figsize=(8, 8))

    if points:
        x_all, y_all = zip(*points)
        ax.scatter(x_all, y_all, c='lightgray', label='Всі точки', s=15, zorder=1)

    if found_points:
        x_found, y_found = zip(*found_points)
        ax.scatter(x_found, y_found, c='red', label='Усередині круга', s=25, zorder=2)

    circle = plt.Circle(center, radius, color='blue', fill=False, linestyle='-', linewidth=2, label='Область пошуку',
        zorder=3)
    ax.add_patch(circle)

    ax.set_aspect('equal', adjustable='datalim')
    plt.legend()
    plt.title(f'Регіональний пошук (знайдено точок: {len(found_points)})')
    plt.xlabel('Вісь X')
    plt.ylabel('Вісь Y')
    plt.grid(True, linestyle=':', alpha=0.6)

    print("\nГрафік створено")
    plt.show()


def get_points():
    while True:
        print("\n--- ПІДГОТОВКА ДАНИХ ---")
        print("1. Згенерувати випадкові точки")
        print("2. Зчитати з файлу (points.txt)")
        choice = input("Оберіть варіант (1/2): ")

        if choice == '1':
            try:
                n = int(input("Введіть кількість точок: "))
                points = [(random.uniform(-100, 100), random.uniform(-100, 100)) for _ in range(n)]
                print(f"[+] Успішно згенеровано {n} точок")
                return points
            except ValueError:
                print("[-] Помилка: введіть ціле число")

        elif choice == '2':
            if not os.path.exists("points.txt"):
                print(
                    "Файл points.txt не знайдено. Створіть його, кожна точка з нового рядка. Наприклад: 1.5 2.0")
                continue
            try:
                points = []
                with open("points.txt", 'r') as f:
                    for line in f:
                        if line.strip():
                            x, y = map(float, line.split())
                            points.append((x, y))
                print(f"Успішно зчитано {len(points)} точок з файлу")
                return points
            except Exception as e:
                print(f"Помилка читання файлу: {e}")
        else:
            print("Некоректний вибір")


def main():
    print("Лабораторна робота: Регіональний пошук для круга")

    points = get_points()
    if not points:
        return

    print("\nПобудова k-d дерева...")
    kdtree = build_kdtree(points)
    print("[+] Дерево успішно побудовано")

    while True:
        print("\n--- МАСОВИЙ ЗАПИТ ---")
        try:
            cx = float(input("Введіть X центру круга (або будь-яку літеру для виходу): "))
            cy = float(input("Введіть Y центру круга: "))
            r = float(input("Введіть радіус R: "))

            if r < 0:
                print("Радіус не може бути від'ємним")
                continue

            center = (cx, cy)

            found = search_circle(kdtree, center, r)
            print(f"Пошук завершено. Знайдено точок: {len(found)}")

            visualize(points, found, center, r)

        except ValueError:
            print("Вихід з програми")
            break


if __name__ == "__main__":
    main()