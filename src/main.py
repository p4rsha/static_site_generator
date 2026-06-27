from textnode import TextType , TextNode



def main():
    dummy = TextNode('some anchor text' , TextType.LINK , 'https://www.boot.dev')
    print(dummy)


if __name__ == '__main__':
    main()