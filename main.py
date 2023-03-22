from jinja2 import Environment, FileSystemLoader
import pdfkit
import copy;

"""
    TODO : 
        1. DONE : Multiple Pages 
        2. DONE : Header
        3. DONE : Footer 
        4. DONE : Image Resolve
        5. DONE : Table Break
        6. DONE : Proper Input
        7. DONE : Table Border
        8. Write Relevant Macros
        9. Fix page-break
        10. change range loop to for each loop : use jinja2 varianles
   <ul>
{% for user in users %}
    <li>{{ user.username|e }}</li>
{% else %}
    <li><em>no users found</em></li>
{% endfor %}
</ul>     
"""


def generateTableData(N):
    notAvailable = "/home/farhaangazi/Projects/Increff/PdfGeneration/main/pdfResources/image-not-available.jpg"
    topSellerStyleLevelPdfRowList = [
        {"style" : "ADFEWRQ120874210", "imageUrl" : notAvailable, 
         "healthyRos" : 2.2, "doh" : 50, "mrp" : 1799.00, 
         "str" : 100, "rawSalesQty" : 100, "revenue" : 202.2, 
         "avgHealthyDaysLive" : 20, "avgRawDaysLive" : 20, 
         "closingStock" : 10, "averageDiscountPercentage" : 20.5, "noOfStores" : 20 }
    ]
    for i in range(N-1):
        sample = copy.deepcopy(topSellerStyleLevelPdfRowList[0])
        sample["style"] = str(i);
        sample["doh"] = sample["doh"]+i;
        topSellerStyleLevelPdfRowList.append(sample);

    if(N==0):
        return []
    return topSellerStyleLevelPdfRowList

def generateParams():
    params = {
        "start_date" : "11-01-23",
        "end_date" : "11-20-23",
        "category" : "category1",
        "channel" : "channel1",
        "attribute1" : "attribute1",
        "attribute2" : "attribute2",
        "season" : "summer-spring",
        "brand" : "brand1",
        "gender" : "male",
        "style_tag" : "NOT SELECTED",
        "sort_by" : "ros_dec",
        "minLiveDays" : "0",
        "minStrPercentage" : "20.20",
        "maxStrPercentage" : "50.5"
    }
    return params;

def main():
    params = generateParams();
    results = generateTableData(40);
    increffLogoUrl = "/home/farhaangazi/Projects/Increff/PdfGeneration/main/pdfResources/increff_image.jpg";
    data = {
            "params" : params,
            "results" : results,
            "increffLogo" : increffLogoUrl
    }
    getPdfFromHTML(data)

def getPdfFromHTML(data):
    environment = Environment(loader=FileSystemLoader("./"))

    #content
    template = environment.get_template("./pdfResources/top-seller-report.html")
    content = template.render( data )

    # with open("generated_pdf_rendered.html", "w") as file:
    #     file.write(content)

    # Header
    header_template = environment.get_template("./pdfResources/header.html")
    header_data = { "increffLogo" : data["increffLogo"] }
    header_content = header_template.render(header_data)
    with open("./pdfResources/header_rendered.html", "w") as file:
        file.write(header_content)

    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
    pdfkit.from_string(content, 'pdf_generated.pdf', configuration=config)

main()