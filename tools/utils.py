
def compress_html(content, use_compress=True):
    if use_compress:
        return content

    # 移除注释
    content = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)
    # 移除换行和制表符
    content = re.sub(r"[\n\t]+", "", content)
    # 移除多余空格（保留属性分隔空格）
    content = re.sub(r"\s+", " ", content)
    # 移除=、>、<、;、: 前后的空格
    content = re.sub(r"\s*([=><;,:])\s*", r"\1", content)
    # 移除标签间空格
    content = re.sub(r">\s+<", "><", content)
    return content


def decompress_html(compressed_content, use_compress=True):
    """
    格式化 HTML 内容，处理压缩和未压缩 HTML，确保输出的内容适合网页渲染。

    参数：
        compressed_content (str): 输入的 HTML 字符串
        use_compress (bool): 是否作为压缩 HTML 处理（True）或直接返回（False）

    返回：
        str: 格式化后的 HTML 字符串
    """
    # 如果 use_compress 为 False 或内容已格式化（有换行和缩进），直接返回
    if not use_compress or re.search(r"\n\s{2,}", compressed_content):
        return compressed_content.strip()

    try:
        # 使用 lxml 解析器处理 HTML，支持不规范的 HTML
        soup = BeautifulSoup(compressed_content, "lxml")

        # 移除多余空白和注释，清理输出
        for element in soup.find_all(text=True):
            if element.strip() == "":
                element.extract()  # 移除空文本节点
            elif element.strip().startswith("<!--") and element.strip().endswith("-->"):
                element.extract()  # 移除注释

        # 判断是否为 HTML 片段（无 DOCTYPE 或 <html> 标签）
        is_fragment = not (
            compressed_content.strip().startswith("<!DOCTYPE")
            or compressed_content.strip().startswith("<html")
        )

        if is_fragment:
            # 对于片段，避免包裹 <html> 或 <body> 标签
            formatted_lines = []
            for child in soup.contents:
                if hasattr(child, "prettify"):
                    formatted_lines.append(child.prettify().strip())
                else:
                    formatted_lines.append(str(child).strip())
            return "\n".join(line for line in formatted_lines if line)

        # 对于完整 HTML 文档，返回格式化输出
        return soup.prettify(formatter="minimal").strip()

    except Exception as e:  # noqa 841
        # 错误处理：解析失败时返回原始内容
        return compressed_content.strip()