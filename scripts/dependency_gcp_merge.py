if __name__ == "__main__":
    with open("source/thirdparty/dss.rst", "r") as f:
        lines = f.readlines()

    outputs = []
    outputs.append(":orphan:\n\n")
    for line in lines:
        if ".. include:: " not in line:
            outputs.append(line)
        else:
            to_include = line.replace(".. include:: ", "").strip()
            to_include = to_include.replace("../", "source/")
            with open(to_include, "r") as f:
                outputs.extend(f.readlines())

    with open("source/thirdparty/dss_merged.rst", "w") as f:
        f.write("".join(outputs))
