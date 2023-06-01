from flask import Flask,render_template,request,redirect,url_for,Response
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


def draw_bar(data):
    x = []
    H_score = []
    OTCE = []
    Dice = []
    for lines in data:
        print(lines)
        x.append(lines[0])
        H_score.append(float(lines[1]))
        OTCE.append(float(lines[2]))
        Dice.append(float(lines[3]))
    # print(x)
    # print(Dice)
    result_list = sorted(zip(Dice, OTCE, H_score, x), reverse=True)
    # print(result_list)
    sorted_id = sorted(range(len(Dice)), key = lambda x:Dice[x], reverse=True)
    # print(Dice)
    plt.figure(figsize=(12,8))
    colorlist = ["#6600CC","#6600CC","#6600CC","#CCBBFF", "#6600CC","#CCBBFF","#CCBBFF","#CCBBFF","#CCBBFF","#CCBBFF","#CCBBFF","#CCBBFF","#CCBBFF","#CCBBFF","#CCBBFF","#CCBBFF",]
    '''
    plt.bar(range(len(Dice)), [i for i,_,_,_ in result_list], tick_label=[i for _,_,_,i in result_list], color=colorlist,label="DICE")  
    plt.xlabel("source name")
    plt.ylabel("Dice")
    plt.ylim(0.55,0.75)
    plt.legend(loc="upper left")
    plt.xticks(rotation=60) 

    '''
    # ax2 = plt.twinx()
    # ax2.set_ylim(-0.05,-0.02)
    # ax2.set_ylabel("OTCE")
    plt.xlabel("source name")
    plt.ylabel("OTCE")
    plt.ylim(-0.05,-0.02)
    plt.legend(loc="upper left")
    plt.xticks(rotation=60) 
    name = [i for _,_,_,i in result_list]
    otce = [i for _,i,_,_, in result_list]
    print(name)
    print(otce)
    plt.plot(name, otce, color="#6600CC", ms=10, lw=1, marker='o',label="OTCE")
    plt.legend(loc="upper right")
    plt.savefig("static/images/demo/line_plot.png")


# target task=ET-22-T2
mod_ana = [
            ["static/images/demo/final/ED-14-T1.jpg", "static/images/demo/final/ED-14-T2.jpg", "static/images/demo/final/NCR-14-T1.jpg", "static/images/demo/final/NCR-14-T2.jpg", ],
            ["static/images/demo/final/ED-13-T1.jpg", "static/images/demo/final/ED-13-T2.jpg", "static/images/demo/final/NCR-13-T1.jpg", "static/images/demo/final/NCR-13-T2.jpg", ], 
            ["static/images/demo/final/ED-17-T1.jpg", "static/images/demo/final/ED-17-T2.jpg", "static/images/demo/final/NCR-17-T1.jpg", "static/images/demo/final/NCR-17-T2.jpg",], 
            ["static/images/demo/final/ED-18-T1.jpg", "static/images/demo/final/ED-18-T2.jpg", "static/images/demo/final/NCR-18-T1.jpg", "static/images/demo/final/NCR-18-T2.jpg",], 
          ]
mod_name = [
                ["ED-14-T1", "ED-14-T2", "NCR-14-T1", "NCR-14-T2"], 
                ["ED-13-T1", "ED-13-T2", "NCR-13-T1", "NCR-13-T2"], 
                ["ED-17-T1", "ED-17-T2", "NCR-17-T1", "NCR-17-T2"], 
                ["ED-18-T1", "ED-18-T2", "NCR-18-T1", "NCR-18-T2"],
            ]
roi_ana = [
            ["ED-14-T2",  "NCR-14-T2", "ED-13-T2", "NCR-13-T2",],
            ["static/images/demo/gt_ed/14.jpg", "static/images/demo/gt_ncr/14.jpg", "static/images/demo/gt_ed/13.jpg", "static/images/demo/gt_ncr/13.jpg",],
            ["0.923", "0.957", "0.882", "0.957",],
            ["ED-17-T2", "NCR-17-T2", "ED-18-T2", "NCR-18-T2",],
            ["static/images/demo/gt_ed/17.jpg", "static/images/demo/gt_ncr/17.jpg","static/images/demo/gt_ed/18.jpg", "static/images/demo/gt_ncr/18.jpg",],
            ["0.846", "0.947", "0.849", "0.947",],
        ]
trans_data = [
                ["ED-14-T2","ED-13-T2","ED-17-T2","ED-18-T2",],
                ["static/images/demo/gt_ed/14.jpg", "static/images/demo/gt_ed/13.jpg", "static/images/demo/gt_ed/17.jpg", "static/images/demo/gt_ed/18.jpg", ],
                ["0.1887", "1.4031", "1.3327", "0.2776",],
                ["-0.0226", "-0.0356", "-0.0389","-0.0273",],
            ]
final_results = [
    ["ED-14-T1", "-0.0380", "-0.0395", "0.664", ],
    ["ED-14-T2", "0.1887", "-0.0226", "0.703", ],
    ["NCR-14-T1", "0.8990", "-0.0395", "0.646", ],
    ["NCR-14-T2", "0.5140", "-0.0383", "0.660", ],
    ["ED-13-T1", "0.4142", "-0.0407", "0.657", ],
    ["ED-13-T2", "1.4031", "-0.0356", "0.695", ],
    ["NCR-13-T1", "5.0050", "-0.0407", "0.628", ],
    ["NCR-13-T2", "10.5247", "-0.0401", "0.683", ],
    ["ED-17-T1", "0.3525", "-0.0435", "0.697", ],
    ["ED-17-T2", "1.3327", "-0.0389", "0.708", ],
    ["NCR-17-T1", "1.5211", "-0.0436", "0.612", ],
    ["NCR-17-T2", "6.6535", "-0.0433", "0.681", ],
    ["ED-18-T1", "0.1070", "-0.0435", "0.675", ],
    ["ED-18-T2", "0.2776", "-0.0273", "0.707", ],
    ["NCR-18-T1", "0.9038", "-0.0436", "0.664", ],
    ["NCR-18-T2", "2.2038", "-0.0394", "0.666", ],

]
# roi_pic_dir = ["static/images/demo/gt_ed/14.png", "static/images/demo/gt_ncr/14.png", "static/images/demo/gt_ed/13.png", "static/images/demo/gt_ncr/13.png", "static/images/demo/gt_ed/17.png", "static/images/demo/gt_ncr/17.png","static/images/demo/gt_ed/18.png", "static/images/demo/gt_ncr/18.png", ]

table = {}
table["mod_ana"] = mod_ana
table["mod_name"] = mod_name
table["roi_ana"] = roi_ana
# table["roi_pic_dir"] = roi_pic_dir
table["trans_data"] = trans_data
table["final_results"] = final_results
# print(table)



# target task = ET-20-T1

final_results_ = [
    ["ED-14-T1", "1.5433", "-0.0320", "0.636", ],
    ["ED-14-T2", "0.2268", "-0.0330", "0.609", ],
    ["NCR-14-T1", "3.2383", "-0.0325", "0.560", ],
    ["NCR-14-T2", "2.5139", "-0.0330", "0.627", ],
    ["ED-13-T1", "1.7564", "-0.0333", "0.593", ],
    ["ED-13-T2", "1.3293", "-0.0347", "0.636", ],
    ["NCR-13-T1", "2.4574", "-0.0342", "0.498", ],
    ["NCR-13-T2", "6.5037", "-0.0346", "0.610", ],
    ["ED-17-T1", "2.5901", "-0.0351", "0.680", ],
    ["ED-17-T2", "-3.2459", "-0.0363", "0.571", ],
    ["NCR-17-T1", "25.7285", "-0.0361", "0.581", ],
    ["NCR-17-T2", "40.6843", "-0.0363", "0.532", ],
    ["ED-18-T1", "0.0901", "-0.0357", "0.613", ],
    ["ED-18-T2", "0.3164", "-0.0355", "0.616", ],
    ["NCR-18-T1", "0.2743", "-0.0361", "0.632", ],
    ["NCR-18-T2", "1.6508", "-0.0362", "0.637", ],

]

app = Flask(__name__)
app.debug=True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/demonstration')
def demonstration():
    return render_template('demo.html')


'''@app.route('/demonstration',methods=["GET", "POST"])
def demonstration():
    if request.method == 'POST':
        target_name = request.form.get('targetname')
        print(target_name)
        return render_template('1.html',target_name=target_name)
    draw_bar(table["final_results"])
    return render_template('1.html', tables = table)'''


'''@app.route('/demonstration/<targetname>')
def demon(target_name):
    return render_template('1.html',target_name=target_name)'''


@app.route('/upload')
def upload():
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000)
    #  app.run(host='0.0.0.0',port=15000)

