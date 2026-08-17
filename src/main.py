from textnode import TextNode, textType


def main():
    # Example usage of TextNode
    text_node1 = TextNode("Hello, World!", textType.PLAIN)
    text_node2 = TextNode("This is bold text.", textType.BOLD)
    text_node3 = TextNode("Visit OpenAI", textType.LINK, url="https://www.boot.dev")

    print(text_node1)
    print(text_node2)
    print(text_node3)

if __name__ == "__main__":
    main()