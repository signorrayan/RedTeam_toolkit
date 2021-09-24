import os
import re
from datetime import datetime

from fpdf import FPDF

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class PDF(FPDF):
    def header(self):
        # Logo
        self.image(f"{BASE_DIR}/static/toolkit/images/sidebar_logo.png", 10, 8, 33)

        self.set_font("Arial", "B", 15)
        # Calculate width of title and position
        w = self.get_string_width(title) + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        # 0, 80, 180
        self.set_draw_color(166, 1, 3)
        # 128, 143, 164
        self.set_fill_color(1, 1, 3)
        # 254, 253, 254
        self.set_text_color(254, 253, 254)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(w, 9, title, 1, 1, "C", 1)
        self.ln(3)

        # User
        uw = self.get_string_width(u[0]) + 2
        self.set_x((230 - uw + 1))
        self.set_text_color(1, 1, 3)
        self.set_font("Arial", "I", 9)
        self.cell(uw, -20, u[0])
        uw = self.get_string_width(u[1]) + 2
        self.set_x((204 - uw + 1))
        self.set_text_color(1, 1, 3)
        self.set_font("Arial", "I", 9)
        self.cell(uw, -10, u[1])
        # self.ln(20)

        # Report Type
        rt = self.get_string_width(report_type) + 6
        self.set_x((200 - rt) / 2)
        self.set_text_color(1, 1, 3)
        self.set_font("Arial", "B", 15)
        self.cell(15, 20, report_type, "C", 1)

        # Time
        # _ = self.get_string_width(cdate) + 6
        self.set_text_color(1, 1, 3)
        self.set_x(8)
        self.set_font("Arial", "B", 13)
        self.cell(8, 10, datetime.now().strftime("%Y-%m-%d %H:%M"), "C", 1)
        # Line break
        # self.ln(15)

        # Header Line
        self.set_x(0)
        self.cell(
            0,
            5,
            "______________________________________________________________________________________",
            0,
            1,
        )
        self.ln(5)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font("Arial", "I", 8)
        # Page number
        self.cell(0, 10, "Page " + str(self.page_no()) + "/{nb}", 0, 0, "C")


def convert_to_pdf(output, user_name, ip, function_name):
    import codecs

    with open(f"{BASE_DIR}/static/toolkit/c.bin", "r") as n:
        n = codecs.decode(n.readline().rstrip(), "hex").decode("utf-8")

    pdf = PDF()
    global title, report_type, u
    u = str(n).split(",")
    report_type = f"[ {str(function_name).upper()} ]"
    title = ip
    directory = f"{BASE_DIR}/media/toolkit/reports/{user_name}"
    os.makedirs(directory, exist_ok=True)

    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_text_color(1, 1, 3)

    for line in output:
        if function_name == "fullscan":
            pdf.set_font("Times", "B", 11) if "/tcp" in line else pdf.set_font(
                "Times", "", 10
            )
        else:
            pdf.set_font(
                "Times", "B", 11
            ) if "scan report for" in line else pdf.set_font("Times", "", 10)

        pdf.cell(0, 7, line, 0, 1)

    if re.match(r"[\d\.]+\/\d+", str(ip)):
        ip = str(ip).split("/")[0]
    elif re.match(r"http\w?\://\S+", str(ip)):
        ip = str(ip).split("/")[2]

    pdf.output(f"{directory}/{function_name}-{str(ip)}.pdf", "F")
