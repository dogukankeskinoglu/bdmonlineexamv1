var question_no = 1;
var choice_no = 1;
var delete_question_no = 0;
var delete_bool = false;
var temp_question_no = -1;

function addQuestion() {
    //<img src="" alt="">
    var exam_div = $("#exams")
    var line_blank = $("<br>")

    var trash_button = $(`<button type="button " class="trashbutton" onclick="deleteQuestion()"></button>`)
    trash_button.attr("style", "padding:8px")

    var trash_img = $('<img  alt="resim bulunamadı">')

    trash_img.attr("src", "../static/images/trash.png")
    trash_img.attr("width", "25px")
    trash_img.attr("height", "25px")
    trash_button.append(trash_img)
    var question_div = $("<div></div>")
    question_div.attr("id", "question" + question_no)
    question_div.attr("class", "content")
    var questionheader = $("<h4>Question " + question_no + "</h4>")
    var sorucontent = $(`<textarea name = "textarea"
        placeholder = "Enter your Question here." > </textarea><br>`)
    sorucontent.attr("id", "questioncontent" + question_no)
    question_div.append(questionheader)
    question_div.append(trash_button)
    question_div.append(sorucontent)
    for (var i = 1; i < 6; i++) {
        var choice_radio = $(`<input type="radio">`)
        choice_radio.attr("name", "radiop" + question_no)
        choice_radio.attr("id", "question" + question_no + "choice" + i)
            //<label for="a"></label>
        var choice_radiolabel = $(`<label></label>`)
        choice_radiolabel.attr("for", "question" + question_no + "choice" + i)
        var choice_input = $(`<input type="text">`)
        choice_input.attr("placeholder", i + " choice")
        choice_input.attr("id", "questioninput" + question_no + "choice" + i)
        question_div.append(choice_radio)
        question_div.append(choice_radiolabel)
        question_div.append(choice_input)
    }
    var question_points_div = $("<div></div>")
    var question_points_label = $("<label>Soru puanı</label>")
    var question_points = $(`<input type="text">`)
    question_points_div.append(question_points_label)
    question_points_div.append(question_points)
    question_points.attr("placeholder", "Sorunun punanını giriniz")
    question_points.attr("id", "question" + question_no + "point")
    question_div.append(line_blank)
    question_div.append(question_points_div)
    exam_div.append(question_div)
    choice_no = 1;
    question_no++;
}


function deleteQuestion() {
    console.log("s")
    $(".trashbutton").click(function() {
        delete_bool = true;
        if (question_no <= 1) {
            question_no = 1
        } else {
            question_no--;
        }
        //$(this).parent().closest('div').remove();
        delete_question_no = $(this).parent().closest('div').find("h4").text()
        $(this).parent().closest('div').remove();
    });
    alert(delete_question_no)

}

function finishExam() {
    console.log("girdi");
    var exam_content = document.getElementById("exams")
    var exam = []
    var dogru_cevap_sık = 0;
    var question_content = "";
    var a_choice_content = "";
    var b_choice_content = "";
    var c_choice_content = "";
    var d_choice_content = "";
    var e_choice_content = "";
    var soru_puan = 0;
    var soru_key = "";
    var sınav_toplam_puan = 0;
    for (var i = 1; i < question_no; i++) {
        soru_puan = parseInt(document.getElementById("question" + i + "point").value);
        sınav_toplam_puan += soru_puan;
    }
    if (sınav_toplam_puan > 100) {
        alert("Sınav toplam puanı 100den yüksek olamaz" + sınav_toplam_puan)
            //sınav_toplam_puan = 0;
    } else {
        for (var i = 1; i < question_no; i++) {
            question_content = document.getElementById("questioncontent" + i).value;
            a_choice_content = document.getElementById("questioninput" + i + "choice" + 1).value;
            b_choice_content = document.getElementById("questioninput" + i + "choice" + 2).value;
            c_choice_content = document.getElementById("questioninput" + i + "choice" + 3).value;
            d_choice_content = document.getElementById("questioninput" + i + "choice" + 4).value;
            e_choice_content = document.getElementById("questioninput" + i + "choice" + 5).value;
            //var question = document.getElementById("question" + i)
            soru_puan = document.getElementById("question" + i + "point").value;

            soru_key = "soru" + i;
            for (var k = 1; k < 6; k++) {
                if (document.getElementById("question" + i + "choice" + k).checked) {
                    dogru_cevap_sık = k;
                }
            }
            console.log(question_content)
            console.log(a_choice_content);
            console.log(b_choice_content);
            console.log(c_choice_content);
            console.log(d_choice_content);
            console.log(e_choice_content);
            console.log(dogru_cevap_sık);
            console.log(soru_puan)
            console.log("**")
            var soru_val = {
                a_choice: a_choice_content,
                b_choice: b_choice_content,
                c_choice: c_choice_content,
                d_choice: d_choice_content,
                e_choice: e_choice_content,
                true_answer_choice: dogru_cevap_sık,
                question_point: soru_puan
            };
            exam.push({
                key: soru_key,
                value: soru_val
            })
        }
        for (var key in exam) {
            var value = exam[key];
            console.log(value)
        }
        $.ajax({
            contentType: 'application/json;charset=UTF-8',
            url: "{{url_for('show_exams')}}",
            type: 'POST',
            data: JSON.stringify({
                'data': exam
            }),
            success: function(response) {
                alert("İşlem başarılı!");
                window.location.href = "/exams";
            },
            error: function(error) {
                alert("error");
            }
        });
    }
}