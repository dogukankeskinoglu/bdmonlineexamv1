class Exam:
    exam_id=0
    exam_name=""
    exam_baslama_tarihi=""
    exam_bitis_tarihi=""
    def __init__(self, e_id, e_name,e_baslama_tarihi,e_bitis_tarihi): 
        self.exam_id=e_id
        self.exam_name=e_name
        self.exam_baslama_tarihi=e_baslama_tarihi
        self.exam_bitis_tarihi=e_bitis_tarihi
    def display(self):
        print("sss")