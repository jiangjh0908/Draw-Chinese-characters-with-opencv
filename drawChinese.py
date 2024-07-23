import freetype
import cv2

class put_chinese_text(object):
    def __init__(self, ttf):
        self._face = freetype.Face(ttf)

    def draw_text(self, image, pos, text, text_size, text_color):
        self._face.set_char_size(text_size * 64)
        metrics = self._face.size
        ascender = metrics.ascender / 64.0
        ypos = int(ascender)

        if not isinstance(text, freetype.unicode):
            text = text.decode('utf-8')

        img = self.draw_string(image, pos[0], pos[1] + ypos, text, text_color)
        return img

    def draw_string(self, img, x_pos, y_pos, text, color):
        prev_char = 0
        pen = freetype.Vector()
        pen.x = x_pos << 6  # div 64
        pen.y = y_pos << 6
        hscale = 1.0
        matrix = freetype.Matrix(int(hscale) * 0x10000, int(0.2 * 0x10000), int(0.0 * 0x10000), int(1.1 * 0x10000))
        cur_pen = freetype.Vector()
        pen_translate = freetype.Vector()

        for cur_char in text:
            self._face.set_transform(matrix, pen_translate)
            self._face.load_char(cur_char)
            kerning = self._face.get_kerning(prev_char, cur_char)
            pen.x += kerning.x
            slot = self._face.glyph
            bitmap = slot.bitmap
            cur_pen.x = pen.x
            cur_pen.y = pen.y - slot.bitmap_top * 64
            img = self.draw_ft_bitmap(img, bitmap, cur_pen, color)
            pen.x += slot.advance.x
            prev_char = cur_char

        return img

    def draw_ft_bitmap(self, img, bitmap, pen, color):
        x_pos = pen.x >> 6
        y_pos = pen.y >> 6
        cols = bitmap.width
        rows = bitmap.rows
        glyph_pixels = bitmap.buffer

        for row in range(rows):
            for col in range(cols):
                if glyph_pixels[row * cols + col] != 0:
                    img[y_pos + row][x_pos + col][0] = color[0]
                    img[y_pos + row][x_pos + col][1] = color[1]
                    img[y_pos + row][x_pos + col][2] = color[2]

        return img

# Example usage
font_path = 'simsun.ttc'
ft = put_chinese_text(font_path)
font_size = 34
color = (0, 255, 0)
result = "test test 测试 测试"
img = cv2.imread("down.jpg")
detect = [150, 350]

img_ = ft.draw_text(img, (detect[0], detect[1] - font_size), result, font_size, color)
cv2.imshow("test", img_)
cv2.waitKey(0)
cv2.destroyAllWindows()