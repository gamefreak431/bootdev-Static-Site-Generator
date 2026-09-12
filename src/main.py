from textnode import TextNode, TextType


def main():
    # Example usage of TextNode
    text_node1 = TextNode("Hello, World!", TextType.TEXT)
    text_node2 = TextNode("This is bold text.", TextType.BOLD)
    text_node3 = TextNode("Visit OpenAI", TextType.LINK, url="https://www.boot.dev")

    print(text_node1)
    print(text_node2)
    print(text_node3)

if __name__ == "__main__":
    main()
