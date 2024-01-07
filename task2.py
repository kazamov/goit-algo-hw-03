import turtle


def koch_snowflake(t, order, size):
    for _ in range(3):
        koch_curve(t, order, size)
        t.right(120)


def koch_curve(t, order, size):
    if order == 0:
        t.forward(size)
    else:
        for angle in [60, -120, 60, 0]:
            koch_curve(t, order - 1, size / 3)
            t.left(angle)


def draw_koch_snowflake(order, size=300):
    window = turtle.Screen()
    window.bgcolor("white")

    t = turtle.Turtle()
    t.speed(0)  # Set the drawing speed (0 is the fastest)
    t.penup()

    # Calculate the starting position to center the snowflake
    start_x = -size / 2
    start_y = size / 2 / 3**0.5

    t.goto(start_x, start_y)
    t.pendown()

    koch_snowflake(t, order, size)

    window.mainloop()


if __name__ == "__main__":
    draw_koch_snowflake(3)
