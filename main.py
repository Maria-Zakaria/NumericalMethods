import tkinter as tk
from tkinter import messagebox, ttk

import sympy as sp

from bisection import bisection
from secant import secant
from newton_raphson import newton_raphson
from gauss import gauss
from jacobi import jacobi
from lagrange import lagrange
from differentiation import differentiation


# =========================================================
# ألوان البرنامج
# =========================================================

PRIMARY = "#1D4ED8"
NAVY = "#0F172A"
LIGHT_BLUE = "#EFF6FF"
BACKGROUND = "#F8FAFC"
WHITE = "#FFFFFF"
BORDER = "#CBD5E1"
SUCCESS = "#15803D"
ERROR = "#B91C1C"
GRAY = "#64748B"
TEXT = "#1E293B"

FONT = "Segoe UI"


# =========================================================
# التطبيق الرئيسي
# =========================================================

class NumericalMethodsApp:

    def __init__(self, root):

        self.root = root

        self.root.title(" الطرق العددية")
        self.root.geometry("1100x750")
        self.root.minsize(850, 600)
        self.root.configure(bg=BACKGROUND)

        self.current_method = None

        self.fields = {}

        self.matrix_entries = []
        self.vector_entries = []
        self.initial_entries = []

        self.result_frame = None

        self.size_var = tk.StringVar(value="3")

        self.configure_styles()

        self.show_home()


    # =====================================================
    # إعداد شكل الجداول
    # =====================================================

    def configure_styles(self):

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=WHITE,
            foreground=TEXT,
            fieldbackground=WHITE,
            rowheight=30,
            font=(FONT, 10)
        )

        style.configure(
            "Treeview.Heading",
            background=PRIMARY,
            foreground=WHITE,
            font=(FONT, 10, "bold")
        )

        style.map(
            "Treeview",
            background=[
                ("selected", LIGHT_BLUE)
            ],
            foreground=[
                ("selected", TEXT)
            ]
        )

        style.configure(
            "TCombobox",
            padding=5,
            font=(FONT, 10)
        )


    # =====================================================
    # إنشاء Scroll عام للصفحة
    # =====================================================

    def create_scrollable_area(self):

        container = tk.Frame(
            self.root,
            bg=BACKGROUND
        )

        container.pack(
            fill="both",
            expand=True
        )

        canvas = tk.Canvas(
            container,
            bg=BACKGROUND,
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=canvas.yview
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        content = tk.Frame(
            canvas,
            bg=BACKGROUND
        )

        window_id = canvas.create_window(
            (0, 0),
            window=content,
            anchor="nw"
        )

        def update_scroll_region(event=None):

            canvas.configure(
                scrollregion=canvas.bbox("all")
            )

        content.bind(
            "<Configure>",
            update_scroll_region
        )

        def resize_content(event):

            canvas.itemconfig(
                window_id,
                width=event.width
            )

        canvas.bind(
            "<Configure>",
            resize_content
        )

        # Mouse wheel
        def mouse_wheel(event):

            canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        canvas.bind_all(
            "<MouseWheel>",
            mouse_wheel
        )

        return content


    # =====================================================
    # مسح الشاشة
    # =====================================================

    def clear_screen(self):

        for widget in self.root.winfo_children():
            widget.destroy()


    # =====================================================
    # رأس الصفحة
    # =====================================================

    def header(self, title, subtitle=None):

        frame = tk.Frame(
            self.root,
            bg=WHITE,
            padx=35,
            pady=22
        )

        frame.pack(
            fill="x"
        )

        tk.Label(
            frame,
            text=title,
            bg=WHITE,
            fg=NAVY,
            font=(FONT, 24, "bold")
        ).pack(
            anchor="w"
        )

        if subtitle:

            tk.Label(
                frame,
                text=subtitle,
                bg=WHITE,
                fg=GRAY,
                font=(FONT, 11)
            ).pack(
                anchor="w",
                pady=(5, 0)
            )


    # =====================================================
    # الصفحة الرئيسية
    # =====================================================

    def show_home(self):#الصفحة الرئيسة 

        self.clear_screen()

        self.header(
            "  الطرق العددية",
            "التحليل العددي - الطرق العددية"
        )

        body = self.create_scrollable_area()

        body.configure(
            padx=35,
            pady=24
        )

        self.method_section(
            body,
            "المعادلات غير الخطية والاشتقاق",
            [
                ("طريقة تنصيف الفترة", "bisection"),
                ("طريقة القاطع", "secant"),
                ("طريقة نيوتن", "newton_raphson"),
                ("الاشتقاق", "differentiation"),
            ]
        )

        self.method_section(
            body,
            "الأنظمة الخطية وطرق الاستيفاء",
            [
                ("طريقة جاوس", "gauss"),
                ("طريقة جاكوبي", "jacobi"),
                ("طريقة لاغرانج", "lagrange"),
            ]
        )

        tk.Label(
            body,
            text="Python + Tkinter",
            bg=BACKGROUND,
            fg=GRAY,
            font=(FONT, 10)
        ).pack(
            pady=20
        )


    # =====================================================
    # أقسام الطرق
    # =====================================================

    def method_section(
        self,
        parent,
        title,
        methods
    ):

        section = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=20,
            pady=16
        )

        section.pack(
            fill="x",
            pady=(0, 18)
        )

        tk.Label(
            section,
            text=title,
            bg=WHITE,
            fg=NAVY,
            font=(FONT, 12, "bold")
        ).pack(
            anchor="w",
            pady=(0, 12)
        )

        buttons = tk.Frame(
            section,
            bg=WHITE
        )

        buttons.pack(
            fill="x"
        )

        for title, method in methods:

            button = tk.Button(
                buttons,
                text=title,
                command=lambda m=method: self.show_method(m),#طريقة العرض
                bg=LIGHT_BLUE,
                fg=PRIMARY,
                activebackground=PRIMARY,
                activeforeground=WHITE,
                relief="flat",
                cursor="hand2",
                font=(FONT, 10, "bold"),
                padx=14,
                pady=11
            )

            button.pack(
                side="left",
                fill="x",
                expand=True,
                padx=(0, 10)
            )


    # =====================================================
    # عرض الطريقة
    # =====================================================

    def show_method(self, method):

        self.current_method = method

        self.clear_screen()

        names = {

            "bisection": (
                "طريقة تنصيف الفترة",
                "إيجاد جذر تقريبي بتقسيم الفترة الصحيحة إلى نصفين باستمرار."
            ),

            "secant": (
                "طريقة القاطع",
                "إيجاد جذر تقريبي باستخدام قواطع المنحنى."
            ),

            "newton_raphson": (
                "طريقة نيوتن",
                "إيجاد جذر تقريبي باستخدام الدالة ومشتقتها."
            ),

            "differentiation": (
                "الاشتقاق العددي",
                "حساب المشتقة عددياً عند نقطة معينة."
            ),

            "gauss": (
                "طريقة جاوس",
                "حل نظام خطي باستخدام طريقة الحذف لجاوس."
            ),

            "jacobi": (
                "طريقة جاكوبي",
                "حل نظام خطي باستخدام التحديثات المتزامنة."
            ),

            "lagrange": (
                "طريقة لاغرانج",
                "استيفاء الحدوديات باستخدام نقاط البيانات."
            ),
        }

        title, description = names[method]

        self.header(
            title,
            description
        )

        outer = self.create_scrollable_area()

        outer.configure(
            padx=35,
            pady=18
        )

        if method in (
            "bisection",
            "secant",
            "newton_raphson",
            "differentiation"
        ):

            self.create_root_form(
                outer,
                method
            )

        else:

            self.create_matrix_form(
                outer,
                method
            )


    # =====================================================
    # إنشاء حقل
    # =====================================================

    def labeled_entry(
        self,
        parent,
        label,
        key,
        width=22
    ):

        frame = tk.Frame(
            parent,
            bg=WHITE
        )

        frame.pack(
            side="left",
            padx=(0, 18),
            pady=8
        )

        tk.Label(
            frame,
            text=label,
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 10, "bold")
        ).pack(
            anchor="w"
        )

        entry = tk.Entry(
            frame,
            width=width,
            relief="solid",
            bd=1,
            font=(FONT, 10),
            fg=TEXT
        )

        entry.pack(
            pady=(5, 0),
            ipady=4
        )

        self.fields[key] = entry

        return entry


    # =====================================================
    # نماذج الطرق غير الخطية
    # =====================================================

    def create_root_form(
        self,
        parent,
        method
    ):

        self.fields = {}

        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=20,
            pady=15
        )

        card.pack(
            fill="x"
        )

        row = tk.Frame(
            card,
            bg=WHITE
        )

        row.pack(
            fill="x"
        )

        self.labeled_entry(
            row,
            "الدالة f(x)",
            "function",
            30
        )

        if method == "bisection":

            self.labeled_entry(
                row,
                "القيمة a",
                "a"
            )

            self.labeled_entry(
                row,
                "القيمة b",
                "b"
            )

            self.labeled_entry(
                row,
                "حد الخطأ",
                "tolerance"
            )

            self.labeled_entry(
                row,
                "الحد الأقصى للتكرارات",
                "max_iterations"
            )

            examples = (
                "x^3 - x - 2",
                "1",
                "2",
                "0.0001",
                "50"
            )

        elif method == "secant":

            self.labeled_entry(
                row,
                "القيمة x0",
                "x0"
            )

            self.labeled_entry(
                row,
                "القيمة x1",
                "x1"
            )

            self.labeled_entry(
                row,
                "حد الخطأ",
                "tolerance"
            )

            self.labeled_entry(
                row,
                "الحد الأقصى للتكرارات",
                "max_iterations"
            )

            examples = (
                "x^3 - x - 2",
                "1",
                "2",
                "0.0001",
                "50"
            )

        elif method == "newton_raphson":

            self.labeled_entry(
                row,
                "القيمة الابتدائية x0",
                "x0"
            )

            self.labeled_entry(
                row,
                "حد الخطأ",
                "tolerance"
            )

            self.labeled_entry(
                row,
                "الحد الأقصى للتكرارات",
                "max_iterations"
            )

            examples = (
                "x^3 - 2*x^2 + x - 3",
                "2",
                "0.0001",
                "50"
            )

        elif method == "differentiation":

            self.labeled_entry(
                row,
                "نقطة الحساب x",
                "x0"
            )

            self.labeled_entry(
                row,
                "قيمة الخطوة h",
                "tolerance"
            )

            examples = (
                "x^3 + 2*x",
                "1",
                "0.001"
            )

        self.fill_example(
            method,
            examples
        )

        self.add_action_buttons(
            parent,
            self.calculate_root,
            self.clear_inputs
        )


    # =====================================================
    # تعبئة أمثلة
    # =====================================================

    def fill_example(
        self,
        method,
        values
    ):

        if method == "bisection":

            keys = [
                "function",
                "a",
                "b",
                "tolerance",
                "max_iterations"
            ]

        elif method == "secant":

            keys = [
                "function",
                "x0",
                "x1",
                "tolerance",
                "max_iterations"
            ]

        elif method == "newton_raphson":

            keys = [
                "function",
                "x0",
                "tolerance",
                "max_iterations"
            ]

        elif method == "differentiation":

            keys = [
                "function",
                "x0",
                "tolerance"
            ]

        else:

            return

        for key, value in zip(keys, values):

            if key in self.fields:

                self.fields[key].insert(
                    0,
                    value
                )


    # =====================================================
    # نموذج المصفوفات
    # =====================================================

    def create_matrix_form(
        self,
        parent,
        method
    ):

        self.fields = {}

        self.matrix_entries = []
        self.vector_entries = []
        self.initial_entries = []

        controls = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=20,
            pady=14
        )

        controls.pack(
            fill="x",
            pady=(0, 10)
        )

        tk.Label(
            controls,
            text="حجم البيانات / المصفوفة",
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 10, "bold")
        ).pack(
            side="left"
        )

        self.size_var = tk.StringVar(
            value="3"
        )

        size_menu = ttk.Combobox(
            controls,
            textvariable=self.size_var,
            values=("2", "3", "4"),
            state="readonly",
            width=7
        )

        size_menu.pack(
            side="left",
            padx=(10, 20)
        )

        # التصحيح المهم:
        # عند اختيار حجم جديد يتم إعادة بناء الحقول
        size_menu.bind(
            "<<ComboboxSelected>>",
            lambda event: self.build_matrix_inputs()
        )

        self.matrix_method = method

        self.matrix_input_area = tk.Frame(
            parent,
            bg=BACKGROUND
        )

        self.matrix_input_area.pack(
            fill="x",
            pady=5
        )

        self.build_matrix_inputs()

        self.add_action_buttons(
            parent,
            self.calculate_matrix,
            self.clear_inputs
        )


    # =====================================================
    # بناء حقول المصفوفة
    # =====================================================

    def build_matrix_inputs(self):

        for widget in self.matrix_input_area.winfo_children():

            widget.destroy()

        self.matrix_entries = []
        self.vector_entries = []
        self.initial_entries = []

        try:

            size = int(
                self.size_var.get()
            )

        except ValueError:

            size = 3

        card = tk.Frame(
            self.matrix_input_area,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=20,
            pady=14
        )

        card.pack(
            fill="x"
        )

        # =================================================
        # Lagrange
        # =================================================

        if self.matrix_method == "lagrange":

            tk.Label(
                card,
                text="نقاط الاستيفاء (x و y)",
                bg=WHITE,
                fg=NAVY,
                font=(FONT, 11, "bold")
            ).grid(
                row=0,
                column=0,
                columnspan=3,
                sticky="w",
                pady=(0, 8)
            )

            for i in range(size):

                tk.Label(
                    card,
                    text=f"النقطة {i + 1}:",
                    bg=WHITE,
                    fg=TEXT,
                    font=(FONT, 10, "bold")
                ).grid(
                    row=i + 1,
                    column=0,
                    sticky="w",
                    pady=4
                )

                row_entries = []

                for j in range(2):

                    entry = self.small_entry(
                        card
                    )

                    entry.grid(
                        row=i + 1,
                        column=j + 1,
                        padx=5,
                        pady=4
                    )

                    row_entries.append(
                        entry
                    )

                self.matrix_entries.append(
                    row_entries
                )

            settings = tk.Frame(
                card,
                bg=WHITE
            )

            settings.grid(
                row=size + 1,
                column=0,
                columnspan=3,
                sticky="w",
                pady=(14, 0)
            )

            self.labeled_entry(
                settings,
                "قيمة x المراد حسابها",
                "tolerance",
                12
            )

            self.fields[
                "tolerance"
            ].insert(
                0,
                "2.5"
            )

            return

        # =================================================
        # Matrix A
        # =================================================

        tk.Label(
            card,
            text="المصفوفة A",
            bg=WHITE,
            fg=NAVY,
            font=(FONT, 11, "bold")
        ).grid(
            row=0,
            column=0,
            columnspan=size,
            sticky="w",
            pady=(0, 8)
        )

        for i in range(size):

            row_entries = []

            for j in range(size):

                entry = self.small_entry(
                    card
                )

                entry.grid(
                    row=i + 1,
                    column=j,
                    padx=4,
                    pady=3
                )

                row_entries.append(
                    entry
                )

            self.matrix_entries.append(
                row_entries
            )

        # =================================================
        # Vector B
        # =================================================

        vector_column = size + 1

        tk.Label(
            card,
            text="المتجه B",
            bg=WHITE,
            fg=NAVY,
            font=(FONT, 11, "bold")
        ).grid(
            row=0,
            column=vector_column,
            sticky="w",
            padx=(25, 0),
            pady=(0, 8)
        )

        for i in range(size):

            entry = self.small_entry(
                card
            )

            entry.grid(
                row=i + 1,
                column=vector_column,
                padx=(25, 4),
                pady=3
            )

            self.vector_entries.append(
                entry
            )

        # =================================================
        # Initial Guess - Jacobi
        # =================================================

        if self.matrix_method == "jacobi":

            initial_column = size + 2

            tk.Label(
                card,
                text="التخمين الابتدائي",
                bg=WHITE,
                fg=NAVY,
                font=(FONT, 11, "bold")
            ).grid(
                row=0,
                column=initial_column,
                sticky="w",
                padx=(25, 0),
                pady=(0, 8)
            )

            for i in range(size):

                entry = self.small_entry(
                    card
                )

                entry.grid(
                    row=i + 1,
                    column=initial_column,
                    padx=(25, 4),
                    pady=3
                )

                self.initial_entries.append(
                    entry
                )

            settings = tk.Frame(
                card,
                bg=WHITE
            )

            settings.grid(
                row=size + 1,
                column=0,
                columnspan=size + 3,
                sticky="w",
                pady=(14, 0)
            )

            self.labeled_entry(
                settings,
                "حد الخطأ المسموح",
                "tolerance",
                12
            )

            self.labeled_entry(
                settings,
                "الحد الأقصى للتكرارات",
                "max_iterations",
                12
            )

            self.fields[
                "tolerance"
            ].insert(
                0,
                "0.0001"
            )

            self.fields[
                "max_iterations"
            ].insert(
                0,
                "50"
            )


    # =====================================================
    # حقل صغير
    # =====================================================

    def small_entry(
        self,
        parent
    ):

        return tk.Entry(
            parent,
            width=9,
            relief="solid",
            bd=1,
            font=(FONT, 10)
        )


    # =====================================================
    # أزرار العمليات
    # =====================================================

    def add_action_buttons(
        self,
        parent,
        calculate_command,
        clear_command
    ):

        bar = tk.Frame(
            parent,
            bg=BACKGROUND
        )

        bar.pack(
            fill="x",
            pady=(18, 20)
        )

        # زر الرجوع

        tk.Button(
            bar,
            text="رجوع",
            command=self.show_home,
            bg=WHITE,
            fg=TEXT,
            activebackground=LIGHT_BLUE,
            relief="solid",
            bd=1,
            font=(FONT, 10, "bold"),
            padx=20,
            pady=9,
            cursor="hand2"
        ).pack(
            side="left"
        )

        # زر المسح

        tk.Button(
            bar,
            text="مسح",
            command=clear_command,
            bg=WHITE,
            fg=TEXT,
            activebackground=LIGHT_BLUE,
            relief="solid",
            bd=1,
            font=(FONT, 10, "bold"),
            padx=20,
            pady=9,
            cursor="hand2"
        ).pack(
            side="right",
            padx=(10, 0)
        )

        # زر الحساب

        tk.Button(
            bar,
            text="احسب",
            command=calculate_command,
            bg=PRIMARY,
            fg=WHITE,
            activebackground=NAVY,
            relief="flat",
            cursor="hand2",
            font=(FONT, 10, "bold"),
            padx=25,
            pady=10
        ).pack(
            side="right"
        )


    # =====================================================
    # مسح البيانات
    # =====================================================

    def clear_inputs(self):

        for entry in self.fields.values():

            if isinstance(entry, tk.Entry):

                entry.delete(
                    0,
                    tk.END
                )

        for row in self.matrix_entries:

            for entry in row:

                if isinstance(entry, list):

                    for e in entry:

                        e.delete(
                            0,
                            tk.END
                        )

                else:

                    entry.delete(
                        0,
                        tk.END
                    )

        for entry in (
            self.vector_entries +
            self.initial_entries
        ):

            entry.delete(
                0,
                tk.END
            )


        # حذف النتيجة السابقة

        if self.result_frame:

            self.result_frame.destroy()

            self.result_frame = None


    # =====================================================
    # قراءة رقم
    # =====================================================

    def read_float(
        self,
        key,
        label
    ):

        value = self.fields[key].get().strip()

        if not value:

            raise ValueError(
                "يرجى إدخال {}.".format(label)
            )

        try:

            return float(value)

        except ValueError as exc:

            raise ValueError(
                "يرجى إدخال رقم صحيح لـ {}.".format(label)
            ) from exc


    # =====================================================
    # قراءة إعدادات Jacobi
    # =====================================================

    def read_settings(self):

        tolerance = self.read_float(
            "tolerance",
            "حد الخطأ المسموح"
        )

        if tolerance <= 0:

            raise ValueError(
                "يجب أن يكون حد الخطأ أكبر من صفر."
            )

        value = self.fields[
            "max_iterations"
        ].get().strip()

        try:

            max_iterations = int(
                value
            )

        except ValueError as exc:

            raise ValueError(
                "يجب أن يكون الحد الأقصى للتكرارات عددًا صحيحًا موجبًا."
            ) from exc

        if max_iterations <= 0:

            raise ValueError(
                "يجب أن يكون الحد الأقصى للتكرارات عددًا صحيحًا موجبًا."
            )

        return tolerance, max_iterations


    # =====================================================
    # تحليل الدالة
    # =====================================================

    def parse_expression(
        self,
        text,
        variable
    ):

        text = text.strip()

        if not text:

            raise ValueError(
                "يرجى إدخال دالة."
            )

        symbol = sp.Symbol(
            variable
        )

        try:

            expression = sp.sympify(
                text.replace(
                    "^",
                    "**"
                ),
                locals={
                    variable: symbol
                },
                evaluate=True
            )

            return expression, sp.lambdify(
                symbol,
                expression,
                modules=["math"]
            )

        except (
            sp.SympifyError,
            TypeError,
            ValueError
        ) as exc:

            raise ValueError(
                "يرجى إدخال تعبير رياضي صحيح."
            ) from exc


    # =====================================================
    # حساب الطرق غير الخطية
    # =====================================================

    def calculate_root(self):

        try:

            variable = "x"

            expression, function = self.parse_expression(
                self.fields["function"].get(),
                variable
            )

            if self.current_method == "bisection":

                tolerance, max_iterations = self.read_settings()

                a = self.read_float(
                    "a",
                    "a"
                )

                b = self.read_float(
                    "b",
                    "b"
                )

                result = bisection(
                    function,
                    a,
                    b,
                    tolerance,
                    max_iterations
                )

                columns = (
                    "التكرار",
                    "a",
                    "b",
                    "c",
                    "f(c)",
                    "الخطأ"
                )

            elif self.current_method == "secant":

                tolerance, max_iterations = self.read_settings()

                x0 = self.read_float(
                    "x0",
                    "x0"
                )

                x1 = self.read_float(
                    "x1",
                    "x1"
                )

                result = secant(
                    function,
                    x0,
                    x1,
                    tolerance,
                    max_iterations
                )

                columns = (
                    "التكرار",
                    "x_prev",
                    "x_curr",
                    "x_next",
                    "f(x_next)",
                    "الخطأ"
                )

            elif self.current_method == "newton_raphson":

                tolerance, max_iterations = self.read_settings()

                x0 = self.read_float(
                    "x0",
                    "x0"
                )

                derivative = sp.lambdify(
                    sp.Symbol(variable),
                    sp.diff(
                        expression,
                        variable
                    ),
                    modules=["math"]
                )

                result = newton_raphson(
                    function,
                    derivative,
                    x0,
                    tolerance,
                    max_iterations
                )

                columns = (
                    "التكرار",
                    "x",
                    "f(x)",
                    "f'(x)",
                    "الخطأ"
                )

            elif self.current_method == "differentiation":

                x0 = self.read_float(
                    "x0",
                    "نقطة الحساب x"
                )

                h = self.read_float(
                    "tolerance",
                    "قيمة الخطوة h"
                )

                result = differentiation(
                    function,
                    x0,
                    h
                )

                self.show_differentiation_result(
                    result
                )

                return

            self.show_root_result(
                result,
                columns
            )

        except Exception as error:

            messagebox.showerror(
                "خطأ في الحساب",
                translate_error(
                    str(error)
                )
            )


    # =====================================================
    # قراءة المصفوفة
    # =====================================================

    def read_matrix(self):

        try:

            if self.current_method == "lagrange":

                points = []

                for row in self.matrix_entries:

                    x_text = row[0].get().strip()
                    y_text = row[1].get().strip()

                    if not x_text or not y_text:

                        raise ValueError(
                            "يرجى إدخال جميع نقاط الاستيفاء."
                        )

                    x_val = float(
                        x_text
                    )

                    y_val = float(
                        y_text
                    )

                    points.append(
                        (x_val, y_val)
                    )

                target = self.read_float(
                    "tolerance",
                    "قيمة x"
                )

                return points, target

            matrix = [
                [
                    float(
                        entry.get().strip()
                    )
                    for entry in row
                ]
                for row in self.matrix_entries
            ]

            vector = [
                float(
                    entry.get().strip()
                )
                for entry in self.vector_entries
            ]

            initial = [
                float(
                    entry.get().strip()
                )
                for entry in self.initial_entries
            ] if self.initial_entries else []

        except ValueError as exc:

            raise ValueError(
                "يرجى إدخال قيم صحيحة في البيانات."
            ) from exc

        return matrix, vector, initial


    # =====================================================
    # حساب المصفوفات
    # =====================================================

    def calculate_matrix(self):

        try:

            if self.current_method == "lagrange":

                points, target = self.read_matrix()

                result = lagrange(
                    points,
                    target
                )

                self.show_lagrange_result(
                    result
                )

                return

            matrix, vector, initial = self.read_matrix()

            if self.current_method == "gauss":

                result = gauss(
                    matrix,
                    vector
                )

                self.show_direct_result(
                    result
                )

                return

            tolerance, max_iterations = self.read_settings()

            if self.current_method == "jacobi":

                result = jacobi(
                    matrix,
                    vector,
                    initial,
                    tolerance,
                    max_iterations
                )

                self.show_linear_result(
                    result
                )

        except Exception as error:

            messagebox.showerror(
                "خطأ في الحساب",
                translate_error(
                    str(error)
                )
            )


    # =====================================================
    # تجهيز مكان النتيجة
    # =====================================================

    def prepare_result(self):

        if self.result_frame:

            self.result_frame.destroy()

        self.result_frame = tk.Frame(
            self.root,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=18,
            pady=12
        )

        self.result_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 18)
        )

        tk.Label(
            self.result_frame,
            text="نتيجة الحساب",
            bg=WHITE,
            fg=NAVY,
            font=(FONT, 14, "bold")
        ).pack(
            anchor="w",
            pady=(0, 8)
        )

        return self.result_frame


    # =====================================================
    # نتائج الطرق غير الخطية
    # =====================================================

    def show_root_result(
        self,
        result,
        columns
    ):

        frame = self.prepare_result()

        summary = tk.Frame(
            frame,
            bg=WHITE
        )

        summary.pack(
            fill="x",
            pady=(0, 10)
        )

        values = [

            (
                "الجذر التقريبي",
                format_number(
                    result["root"]
                )
            ),

            (
                "عدد التكرارات",
                str(
                    result["iterations"]
                )
            ),

            (
                "الخطأ النهائي",
                format_number(
                    result["error"]
                )
            ),

            (
                "الحالة",
                translate_status(
                    result["status"]
                )
            ),
        ]

        for label, value in values:

            item = tk.Frame(
                summary,
                bg=WHITE
            )

            item.pack(
                side="left",
                padx=(0, 32)
            )

            tk.Label(
                item,
                text=label,
                bg=WHITE,
                fg=GRAY,
                font=(FONT, 9)
            ).pack(
                anchor="w"
            )

            color = (
                SUCCESS
                if label == "الحالة"
                and value == "متقارب"
                else TEXT
            )

            tk.Label(
                item,
                text=value,
                bg=WHITE,
                fg=color,
                font=(FONT, 10, "bold")
            ).pack(
                anchor="w",
                pady=(2, 0)
            )

        self.create_table(
            frame,
            columns,
            result["table"]
        )


    # =====================================================
    # نتيجة Jacobi
    # =====================================================

    def show_linear_result(
        self,
        result
    ):

        frame = self.prepare_result()

        solution = "    ".join(
            "x{} = {}".format(
                i + 1,
                format_number(value)
            )
            for i, value in enumerate(
                result["solution"]
            )
        )

        tk.Label(
            frame,
            text="الحل: " + solution,
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 11, "bold")
        ).pack(
            anchor="w",
            pady=(0, 8)
        )

        status_text = translate_status(
            result["status"]
        )

        status_color = (
            SUCCESS
            if result["status"] == "Converged"
            else ERROR
        )

        tk.Label(
            frame,
            text="الحالة: " + status_text,
            bg=WHITE,
            fg=status_color,
            font=(FONT, 10, "bold")
        ).pack(
            anchor="w",
            pady=(0, 10)
        )

        columns = (
            ("التكرار",)
            +
            tuple(
                "x{}".format(i + 1)
                for i in range(
                    len(result["solution"])
                )
            )
            +
            ("الخطأ",)
        )

        self.create_table(
            frame,
            columns,
            result["table"]
        )


    # =====================================================
    # نتيجة Gauss
    # =====================================================

    def show_direct_result(
        self,
        result
    ):

        frame = self.prepare_result()

        tk.Label(
            frame,
            text="الحل النهائي",
            bg=WHITE,
            fg=NAVY,
            font=(FONT, 12, "bold")
        ).pack(
            anchor="w",
            pady=(0, 8)
        )

        solution = "\n".join(
            "x{} = {}".format(
                i + 1,
                format_number(value)
            )
            for i, value in enumerate(
                result["solution"]
            )
        )

        tk.Label(
            frame,
            text=solution,
            justify="left",
            bg=WHITE,
            fg=TEXT,
            font=(FONT, 10, "bold")
        ).pack(
            anchor="w"
        )

        tk.Label(
            frame,
            text="خطوات الحذف والعمليات",
            bg=WHITE,
            fg=NAVY,
            font=(FONT, 10, "bold")
        ).pack(
            anchor="w",
            pady=(15, 5)
        )

        operations_frame = tk.Frame(
            frame,
            bg=WHITE
        )

        operations_frame.pack(
            fill="both",
            expand=True
        )

        operations_scroll = ttk.Scrollbar(
            operations_frame,
            orient="vertical"
        )

        operations = tk.Text(
            operations_frame,
            height=10,
            wrap="none",
            relief="solid",
            bd=1,
            bg=WHITE,
            fg=TEXT,
            font=("Consolas", 10),
            yscrollcommand=operations_scroll.set
        )

        operations_scroll.configure(
            command=operations.yview
        )

        operations.pack(
            side="left",
            fill="both",
            expand=True
        )

        operations_scroll.pack(
            side="right",
            fill="y"
        )

        operations.insert(
            "1.0",
            format_gauss_operations(
                result["operations"]
            )
            or
            "لم تكن هناك حاجة إلى عمليات."
        )

        operations.configure(
            state="disabled"
        )


    # =====================================================
    # نتيجة الاشتقاق
    # =====================================================

    def show_differentiation_result(
        self,
        result
    ):

        frame = self.prepare_result()

        tk.Label(
            frame,
            text=(
                "قيمة المشتقة الأولى عند النقطة = "
                +
                format_number(
                    result["derivative"]
                )
            ),
            bg=WHITE,
            fg=SUCCESS,
            font=(FONT, 12, "bold")
        ).pack(
            anchor="w",
            pady=10
        )


    # =====================================================
    # نتيجة Lagrange
    # =====================================================

    def show_lagrange_result(
        self,
        result
    ):

        frame = self.prepare_result()

        tk.Label(
            frame,
            text=(
                "قيمة متعددة الحدود للاغرانج عند النقطة = "
                +
                format_number(
                    result["value"]
                )
            ),
            bg=WHITE,
            fg=SUCCESS,
            font=(FONT, 12, "bold")
        ).pack(
            anchor="w",
            pady=10
        )


    # =====================================================
    # إنشاء جدول النتائج
    # =====================================================

    def create_table(
        self,
        parent,
        columns,
        rows
    ):

        table_container = tk.Frame(
            parent,
            bg=WHITE
        )

        table_container.pack(
            fill="both",
            expand=True,
            pady=(5, 0)
        )

        # Scroll رأسي للجدول

        vertical_scroll = ttk.Scrollbar(
            table_container,
            orient="vertical"
        )

        # Scroll أفقي للجدول

        horizontal_scroll = ttk.Scrollbar(
            table_container,
            orient="horizontal"
        )

        tree = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            height=12,
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set
        )

        vertical_scroll.configure(
            command=tree.yview
        )

        horizontal_scroll.configure(
            command=tree.xview
        )

        for column in columns:

            tree.heading(
                column,
                text=column
            )

            tree.column(
                column,
                width=120,
                minwidth=90,
                anchor="center",
                stretch=False
            )

        for row in rows:

            formatted_row = tuple(
                format_number(value)
                for value in row
            )

            tree.insert(
                "",
                "end",
                values=formatted_row
            )

        tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        vertical_scroll.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        horizontal_scroll.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        table_container.grid_rowconfigure(
            0,
            weight=1
        )

        table_container.grid_columnconfigure(
            0,
            weight=1
        )


# =========================================================
# تنسيق الأرقام
# =========================================================
def format_gauss_operations(operations):
    blocks = []
    for op in operations:
        lines = ["الخطوة {}: {}".format(op["step"], op["operation"])]
        for row in op["matrix"]:
            lines.append(
                "    [ " + "  ".join(
                    "{:>10}".format(format_number(v)) for v in row
                ) + " ]"
            )
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)

def format_number(value):

    if isinstance(
        value,
        int
    ):

        return str(value)

    try:

        return "{:.6f}".format(
            float(value)
        )

    except (
        TypeError,
        ValueError
    ):

        return str(value)


# =========================================================
# ترجمة الحالة
# =========================================================

def translate_status(status):

    if status == "Converged":

        return "متقارب"

    if status == "Maximum iterations reached":

        return "تم الوصول إلى الحد الأقصى للتكرارات"

    return status


# =========================================================
# ترجمة الأخطاء
# =========================================================

def translate_error(message):

    translations = {

        "Bisection Method requires opposite signs at a and b.":

            "تتطلب طريقة التنصيف إشارتين مختلفتين عند a و b.",

        "Secant Method requires distinct initial points.":

            "تتطلب طريقة القاطع نقطتين ابتدائيتين مختلفتين.",

        "Newton-Raphson derivative is zero.":

            "مشتقة نيوتن تساوي صفرًا.",

        "Jacobi cannot divide by a zero diagonal value.":

            "لا يمكن لطريقة جاكوبي القسمة على قيمة قطرية تساوي صفرًا.",

        "The matrix is singular and has no unique solution.":

            "المصفوفة مفردة ولا تملك حلًا وحيدًا.",

        "division by zero":

            "حدثت قسمة على صفر.",
    }

    return translations.get(
        message,
        message
    )


# =========================================================
# تشغيل البرنامج
# =========================================================

if __name__ == "__main__":

    application_root = tk.Tk()

    app = NumericalMethodsApp(
        application_root
    )

    application_root.mainloop()