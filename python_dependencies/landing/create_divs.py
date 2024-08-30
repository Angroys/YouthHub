from lxml import etree


def create_div(image_url, title, subtitle):
    div_element = etree.Element("div", attrib={"class": "rectangle"})
    
    img_element = etree.Element("img", attrib={"src": image_url, "alt": "Image"})
    div_element.append(img_element)
    
    text_content = etree.Element("div", attrib={"class": "text-content"})
    
    title_element = etree.Element("div", attrib={"class": "title"})
    title_element.text = title
    
    subtitle_element = etree.Element("div", attrib={"class": "subtitle"})
    subtitle_element.text = subtitle
    
    text_content.append(title_element)
    text_content.append(subtitle_element)
    
    div_element.append(text_content)
    
    return div_element


def edit_html(image, title, subtitle):
    # Parse the existing HTML file
    parser = etree.HTMLParser()
    tree = etree.parse('main.html', parser)

    # Find and modify elements
    title_element = tree.find('.//title')
    if title_element is not None:
        title_element.text = 'New Title'

    # Add a new div
    body = tree.find('body')
    body.append(create_div(image, title, subtitle))

    # Save the updated HTML file
    with open('main.html', 'wb') as file:
        file.write(etree.tostring(tree, pretty_print=True, method="html"))

    print("HTML file updated successfully!")

edit_html("photo.png", "Hello World", "this is a subtitle")