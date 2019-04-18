class ARFFCreator:
    """Creates an correctly formatted ARFF file"""
    # ==== Attributes =====
    file_stream = "" # the file stream to add the the file
    relation_name = "" # the name of the relation added ot file
    attributes = {} # lib of attrs
    attr_order = []
    header_created = 0;

    def __init__(self, output_file, relation_name):
        self.file_stream = open(output_file, 'w') # opens the file stream, clears the file
        self.output_file = output_file
        self.relation_name = relation_name

    #  PRE: none
    # POST: (str) output_file
    def get_output_file(self):
        return self.output_file

    #  PRE: none
    # POST: (str) relation_name
    def get_relation_name(self):
        return self.relation_name

    #  PRE: (str) title of attr
    # POST: adds attr to dictionary as numeric
    def add_numeric_attr(self, title):
        if(self.header_created == 0):
            self.attributes[title] = ['numeric'];
            self.attr_order.append(title)
        else:
            print("Header already added, can only add data")

    #  PRE: (str) title of attr
    # POST: adds attr to dictionary as numeric
    def add_nominal_attr(self, title, array):
        if(self.header_created == 0):
            self.attributes[title] = array;
            self.attr_order.append(title)
        else:
            print("Header already added, can only add data")

    def add_header(self):
        self.header_created = 1;
        self.file_stream.write('%\n%\n% add extra comments here\n%\n%\n\n')

        self.file_stream.write('@relation ' + self.relation_name + '\n\n')
        # Iterating over keys
        # for attr in self.attributes:
        for i in range (len(self.attr_order)):
            attr = self.attr_order[i]
            self.file_stream.write('@attribute ' + attr + ' ')
            if(len(self.attributes[attr]) == 1):
                # ASSERT: if the length of array is 1, {} are not needed
                self.file_stream.write(self.attributes[attr][0])
            else:
                self.file_stream.write('{')
                for i in range(0, len(self.attributes[attr]), 1):
                    self.file_stream.write(self.attributes[attr][i])
                    if(i != len(self.attributes[attr])-1):
                        self.file_stream.write(', ')
                self.file_stream.write('}')
            self.file_stream.write('\n')
        self.file_stream.write('\n@data \n')

    #  PRE: takes a dictionary of values to add to the file, key is the attr is represents
    #       value is the value that represents that attr
    # POST: prints the data in correct format and order
    def add_data(self, dict):
        invalid_data = 0
        data_str = '';
        if(self.header_created != 1):
            print('Must create and call add header to add data')
        else:
            for i in range (len(self.attr_order)):
                attr = self.attr_order[i]
                # print (attr)
                #ASSERT: check in the attr is in the given array
                if attr in dict:
                    #ASSERT: will remove the last comma when added to data
                    if(len(self.attributes[attr]) == 1):
                        data_str = data_str + str(dict[attr]) + ','
                    else:
                        if dict[attr] in self.attributes[attr]:
                            data_str = data_str + dict[attr] + ','
                        elif(dict[attr] == '?'):
                            data_str = data_str + dict[attr] + ','
                        else:
                            invalid_data = 1
                else:
                    invalid_data = 1
        if(invalid_data == 0):
            #ASSERT: [:-1] remove the last unneeded comma
            self.file_stream.write(data_str[:-1] + '\n')
        else:
            print("Not all attr where included into dict")

    def end(self):
        self.file_stream.close() 

# arff = ARFFCreator("text.txt", 'Some-Name')
# arff.add_numeric_attr("distance")
# arff.add_nominal_attr('land-use', ['urban', 'veg', 'water'])
# arff.add_header()
# arff.add_data({'distance' : 1, 'land-use' : 'urban'})
