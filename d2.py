import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


def draw_scaled_ellipse(
    ax,
    center,
    count,
    scale=0.5,
    aspect_ratio=1.0,
    color="blue",
    label="",
    use_log_scale=True,
):
    """
    Draws an ellipse on the given Axes 'ax' with an area based on a transformed count.

    Parameters:
      - ax: matplotlib Axes to draw on.
      - center: (x, y) tuple for the ellipse center.
      - count: The numerical value representing the set size.
      - scale: A scaling factor for the ellipse size.
      - aspect_ratio: Ratio of width/height (1.0 for a circle).
      - color: Fill color of the ellipse.
      - label: Text label to display at the center.
      - use_log_scale: If True, uses a logarithmic transformation to compress
                       differences in counts.
    """
    # Optionally transform the count for visualization purposes.
    if use_log_scale:
        # Using log(count+1) ensures that even a very high count doesn't dominate.
        transformed_value = np.log(count + 1)
    else:
        transformed_value = count

    # Compute a base "radius" proportional to the square root of the (transformed) count.
    r = np.sqrt(transformed_value) * scale

    # Determine ellipse width and height so that area is proportional to r^2.
    width = 2 * r * np.sqrt(aspect_ratio)
    height = 2 * r / np.sqrt(aspect_ratio)

    ellipse = patches.Ellipse(
        center, width, height, color=color, alpha=0.5, ec="black", lw=1.5
    )
    ax.add_patch(ellipse)

    # Place the label (with the original count) at the center.
    ax.text(
        center[0],
        center[1],
        f"{label}\n{count}",
        ha="center",
        va="center",
        fontsize=10,
        weight="bold",
    )
    return ellipse


def main():
    # --------------------------
    # Set Totals for each set
    # --------------------------
    A_total = 1654
    B_total = 2622
    C_total = 2549
    D_total = 21788

    # --------------------------
    # Create the figure and axes
    # --------------------------
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_aspect("equal")

    # --------------------------
    # Define positions for each set's ellipse
    # --------------------------
    # These positions are chosen to allow some overlap.
    positions = {"A": (4, 6), "B": (6, 6), "C": (4, 4), "D": (6, 4)}

    # --------------------------
    # Draw ellipses for each set using the logarithmic scaling
    # to compress the range of sizes.
    # --------------------------
    draw_scaled_ellipse(
        ax,
        positions["A"],
        A_total,
        scale=0.5,
        aspect_ratio=1.5,
        color="red",
        label="A",
        use_log_scale=True,
    )
    draw_scaled_ellipse(
        ax,
        positions["B"],
        B_total,
        scale=0.5,
        aspect_ratio=1.5,
        color="green",
        label="B",
        use_log_scale=True,
    )
    draw_scaled_ellipse(
        ax,
        positions["C"],
        C_total,
        scale=0.5,
        aspect_ratio=1.5,
        color="blue",
        label="C",
        use_log_scale=True,
    )
    draw_scaled_ellipse(
        ax,
        positions["D"],
        D_total,
        scale=0.5,
        aspect_ratio=1.5,
        color="orange",
        label="D",
        use_log_scale=True,
    )

    # --------------------------
    # Adjust plot limits, title, and display the diagram.
    # --------------------------
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    plt.title("4-Set Venn Diagram with Ellipse Areas Based on Transformed Counts")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.show()


if __name__ == "__main__":
    main()
