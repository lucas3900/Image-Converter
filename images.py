"""
 *****************************************************************************
   FILE:        images.py

   AUTHOR:      Lucas Barusek

   DATE:        10/20/18  

   DESCRIPTION: Print and image by converting a list of ppm data to a list
                of tuples Yertle the turtle can draw. This program will
                also be able to print the image in grayscale, negative, and 
                print it blurry by modifying the list of red, green, blue 
                pixel values.


 *****************************************************************************
"""

import turtle
import sys     # for giving file name on command line


def read_file_lines(filename):
    """ Opens and reads a file.  Returns a list of lines from the file. """
    # make sure we can open the file for reading
    file = open(filename)
    assert file

    # Get all the lines and remove the trailing newlines
    lines = file.readlines()
    file.close()
    for i in range(len(lines)):
        lines[i] = lines[i][:-1]
    return lines


def ppm_data_to_image(image):
    """ Takes the ppm date, and converts it to a nested list of tuples
    suitable to be used in draw_image """

    # defines a list to compile the red, green, blue tuples
    triples_list = []

    # finds the width dimension of the image (the length dimension
    # will come automatically in the for loop)
    width = int(image[2][:image[2].index(' ')])

    #splices off all non red, green, blue values
    image = image[4:]

    # While loop iterates for as long as there is three or more numbers
    # in the ppm data.
    while len(image) >= 3:

        # creates a new row each time the while loop iterates
        one_row = []

        # for loop iterates for the length of the list, which will 
        # compile a nested list in accordance with the dimensions 
        # of the image
        for _ in range(width):

            # appends the first three items in the ppm data to one_row as
            # a tuple, and then splices off the first three items in ppm data
            one_row.append((int(image[0]), int(image[1]), int(image[2])))
            image = image[3:]

        # appends each row to the triples list to create the nested list
        triples_list.append(one_row)

    return triples_list


def draw_image(yertle, image):
    """ From the nested list of tuples, yertle the turtle will draw
    the image from each red, green and blue value in each tuple. """

    # creates a nested for loop that iterates for each row and column
    # in the image
    for i in range(len(image)):
        for j in range(len(image[i])):

            # Yertle will draw each pixel, and then move forward one pixel
            yertle.dot(1, image[i][j][0], image[i][j][1], image[i][j][2])
            yertle.forward(1)

        # resets Yertle to the left side of the image, and moves it down
        # one row to draw another column
        yertle.backward(len(image[0]))
        yertle.right(90)
        yertle.forward(1)
        yertle.left(90)


def grayscale(image):
    """ Converts the image to Grayscale by taking the average of the red,
     green, and blue values in each tuple """

    # Defines a list to compile each row of the grayscale image 
    grayscale_image = []

    # iterates through the length of the image
    for i in range(len(image)):

        # creates a new row 
        one_row = []

        # iterates for the width of the image
        for j in range(len(image[i])):

            # Calculates the average of the red, green, and blue, values, and 
            # converts every number in the tuple to that number
            new_pixel = (image[i][j][0] + image[i][j][1] + image[i][j][2]) // 3
            one_row.append((new_pixel, new_pixel, new_pixel))
        
        # appends each row to the grayscale image
        grayscale_image.append(one_row)
    
    return grayscale_image


def negative(image):
    """Convert the image to negative to by subtracting each red, green
    and blue value from 255 to get its negative value. """

    # defines a list to compile each row of the negative image 
    negative_image = []

    # iterates through the length of the image
    for i in range(len(image)):

        # creates a new row
        one_row = []

        # iterates for length of the column
        for j in range(len(image[i])):

            # appends the negative pixel by subtracting the red, green
            # and blue values from 255
            one_row.append((255 - image[i][j][0],
                            255 - image[i][j][1],
                            255 - image[i][j][2]))

        # appends each row to negative image 
        negative_image.append(one_row)

    return negative_image


def calculate_averages(pixel_neighbors):
    """ From the list of neighbors, takes the average of each red,
    green, and blue value and returns the averaged pixel"""

    # defines variable to be used to calculate the sum of the red,
    # green, ane blue color values
    red_sum = 0
    green_sum = 0
    blue_sum = 0

    # iterates through all the neigbors in the pixel_neighbors list
    for num in pixel_neighbors:

        # indexes each tuple at the 0, 1, and 2, to isolate the red,
        # green, and blue color values, and adds them up independently
        red_sum += num[0]
        green_sum += num[1]
        blue_sum += num[2]

    # Calculates the average red, green, and blue values by dividing
    # the red, green, and blue sums by the amount of neighbors
    average_red = red_sum // len(pixel_neighbors)
    average_green = green_sum // len(pixel_neighbors)
    average_blue = blue_sum // len(pixel_neighbors)


    return (average_red, average_green, average_blue)


def is_in_bounds(image, row, col):
    """Checks if the location of the neighbor is in bounds"""

    # if statement checks if neighbor is out bounds and returns
    # false if it is
    if row < 0 or row >= len(image) or \
       col < 0 or col >= len(image[0]):
        return False
    
    #returns true if neighbor is in bounds
    return True


def search_neighbors(row, col, image):
    """For each pixel, searches in all directions for all neighboring
    pixels, and if they are within the bounds of the image, returns
    the red, green, and blue color values of that pixel"""

    # defines all the directions to search for, including the 
    # starting position
    directions = [(0, 0), (-1, 0), (-1, 1), (0, 1), (1, 1),
                  (1, 0), (1, -1), (0, -1), (-1, -1)]

    # defines an empty list that will later compile all the neighbors
    neighbor_list = []

    # Makes a copy of the row and column as to not modify the original
    new_row = row
    new_col = col

    # for loop iterates for every possible direction a neighbor could be,
    # and isolates the row direction and the column direction
    for direction in directions:
        row_shift = direction[0]
        col_shift = direction[1]

        # applies the row and column shift to the row and column of
        # the location of the pixel
        neighbor_row = new_row + row_shift
        neighbor_col = new_col + col_shift

        # Calls on is_in_bounds to check if the neighor is in the 
        # bounds of the image. If it is, appends the red, green, blue
        # tuple to neighbor_list
        if is_in_bounds(image, neighbor_row, neighbor_col):
            neighbor_list.append((image[neighbor_row][neighbor_col]))

    return neighbor_list


def blur(image):
    """Makes the image blurry by making each pixel the average of each
    neighboring pixel and itself"""

    # Cite: Peers - Truong Pham and Denzel Capellan
    # Descr: Explained how blur should be doing its job

    # creates a list to compile each row of the blurred image
    blur_list = []

    # iterates through the length of the image
    for i in range(len(image)):

        # creates a new row 
        one_row = []

        # iterates through the width of the image
        for j in range(len(image[i])):

            # calls on search_neighbors to get a list of all the neighboring
            # pixels and the pixel itself
            neighbors = search_neighbors(i, j, image)

            # Calls on calculate_averages to find the average of all the
            # pixels in neighbors
            averages = calculate_averages(neighbors)

            # appends each column
            one_row.append(averages)

        # appends each row
        blur_list.append(one_row)

    return blur_list

        
#------------------------------------------------------------------------
# Main function
#------------------------------------------------------------------------


def main():
    """This is the Main Function"""
    
    # Load the picture data from the file given on
    # the command line.
    if len(sys.argv) != 2:
        print("usage: python3 draw_picture.py FILENAME")
        sys.exit(1)
    filename = sys.argv[1]
    picture = ppm_data_to_image(read_file_lines(filename))

    # Create the turtle/window, and turn off tracing
    yertle = turtle.Turtle()
    turtle.tracer(False)

    # Move turtle to upper left corner
    yertle.up()
    yertle.goto(-390, 340)  # coordinates are a little weird
    yertle.speed(0)

    
    # Apply one or more manipulations, if desired:
    picture = negative(picture)

    picture = grayscale(picture)

    for _ in range(60):  # really blurry!
        picture = blur(picture)

    # # Draw it!

    draw_image(yertle, picture)

    turtle.mainloop()

if __name__ == "__main__":
    main()
