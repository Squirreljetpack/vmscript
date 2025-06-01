import xml.etree.ElementTree as ET
import sys
import copy
import argparse

def merge_block(input_file, block_file, output_file):
    """
    Merge a block XML file into the main XML file.

    This function traverses the block XML tree and adds nodes with attributes
    to the main XML tree. It handles replacing existing elements when a
    'replace' attribute is specified.

    Args:
        input_file (str): Path to main input XML file
        block_file (str): Path to block XML file with elements to merge
        output_file (str): Path to output XML file
    """
    # Parse the main XML file
    with open(input_file, "r") as f:
        main_tree = ET.parse(f)
    main_root = main_tree.getroot()

    # Parse the block XML file
    with open(block_file, "r") as f:
        block_tree = ET.parse(f)
    block_root = block_tree.getroot()

    # Do a DFS of the block tree, and whenever an element with an attribute is encountered, add it to the main tree
    stack = [(block_root, [])]
    while stack:
        node, parent_path = stack.pop()
        if node.attrib:  # This node has attributes
            # Traverse the main tree along parent_path
            current_elem = main_root
            for tag in parent_path[1:]: # do not look for the domain tag
                # Look for a child with the given tag
                next_elem = current_elem.find(tag)
                if next_elem is None:
                    # Create the element without attributes
                    next_elem = ET.Element(tag)
                    current_elem.append(next_elem)
                current_elem = next_elem

            # Remove siblings (children of current_elem) with tag = replace_tag
            if 'replace' in node.attrib:
                replace_tag = node.attrib['replace']
                for child in list(current_elem):
                    if child.tag == replace_tag:
                        current_elem.remove(child)
                # Remove the replace attribute from the node
                del node.attrib['replace']

            # Append a deep copy of the entire node (with subtree) to current_elem
            current_elem.append(copy.deepcopy(node))
        else:
            # This node has no attributes, so process its children
            for child in reversed(node):  # reversed to maintain order
                stack.append((child, parent_path + [node.tag]))

    # Write the modified main tree
    main_tree.write(output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Merge XML block elements into a main XML file.',
        epilog='This script merges the xml in the block_file into the input_file. Any node with an attribute will be directly inserted at the appropriate path. If a "replace=tag_name" attribute is present on the node, it will replace all siblings at its replaced path whose tag type is tag_name.'
    )
    parser.add_argument('input_file', help='Path to main input XML file')
    parser.add_argument('block_file', help='Path to block XML file containing elements to merge')
    parser.add_argument('output_file', nargs='?', help='Path to output XML file (default: overwrites input file)')
    
    args = parser.parse_args()
    
    if args.output_file is None:
        args.output_file = args.input_file
    
    merge_block(args.input_file, args.block_file, args.output_file)
