import numpy as np
import cv2 as cv

def mouse_event_handler(event, x, y, flags, param):
    # Change 'mouse_state' (given as 'param') according to the mouse 'event'
    if event == cv.EVENT_LBUTTONDOWN:
        param[0] = True
        param[1] = (x, y)
    elif event == cv.EVENT_LBUTTONUP:
        param[0] = False
    elif event == cv.EVENT_MOUSEMOVE and param[0]:
        param[1] = (x, y)

def free_drawing(canvas_width=640, canvas_height=480, init_brush_radius=3):
    # Prepare a canvas and palette
    canvas = np.zeros((480, 640, 3), dtype=np.uint8) # Create a color image (black)
    canvas[:] = 255                                  # Make the color image white
    canvas[140:240, 220:420, :] = (255, 255, 0)        # Draw the aqua box
    canvas[240:340, 220:420, :] = (255, 0, 255)        # Draw the magenta box
    palette = [(0, 0, 0), (255, 255, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
    
    # Draw a circle with its label
    center = (100, 240)
    cv.circle(canvas, center, radius=60, color=(0, 255, 0), thickness=5)
    cv.putText(canvas, 'Computer', center, cv.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255))
    
    # Draw a polygon (triangle) with its label
    pts = np.array([(540, 240-50), (540-55, 240+50), (540+55, 240+50)])
    cv.polylines(canvas, [pts], True, color=(0, 255, 255), thickness=5)
    cv.putText(canvas, 'Vision', pts[0].flatten(), cv.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0))
    
    # Initialize drawing states
    mouse_state = [False, (-1, -1)] # Note) [mouse_left_button_click, mouse_xy]
    brush_color = 0
    brush_radius = init_brush_radius

    # Instantiate a window and register the mouse callback function
    cv.namedWindow('Free Drawing')
    cv.setMouseCallback('Free Drawing', mouse_event_handler, mouse_state)

    while True:
        # Draw a point if necessary
        mouse_left_button_click, mouse_xy = mouse_state
        if mouse_left_button_click:
           cv.circle(canvas, mouse_xy, brush_radius, palette[brush_color], -1)

        # Show the canvas
        canvas_copy = canvas.copy()
        info = f'Brush Radius: {brush_radius}'
        cv.putText(canvas_copy, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (127, 127, 127), thickness=2)
        cv.putText(canvas_copy, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, palette[brush_color])
        cv.imshow('Free Drawing', canvas_copy)

        # Process the key event
        key = cv.waitKey(1)
        if key == 27: # ESC
            break
        elif key == ord('\t'):
            brush_color = (brush_color + 1) % len(palette)
        elif key == ord('+') or key == ord('='):
            brush_radius += 1
        elif key == ord('-') or key == ord('_'):
            brush_radius = max(brush_radius - 1, 1)

    cv.destroyAllWindows()

if __name__ == '__main__':
    free_drawing()