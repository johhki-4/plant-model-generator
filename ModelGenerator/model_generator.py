import datetime

# gets the date and time for a unique filename to not overwrite older traces
def getTime():
	timeNow = datetime.datetime.today()
	logName = str(timeNow.year) + "_" + str(timeNow.month) + "_" + str(timeNow.day)
	logName = logName + "_" + str(timeNow.hour) + "_" + str(timeNow.minute)
	return logName

# open the specified file, read the content and put them in a list. entries separated by colon(:)
def readFile(t):
        f = open(t, "r")
        traceList = []
        for line in f:
                splitLine = line.strip()
                splitLine = splitLine.split(":")
                traceList.append(splitLine)
        f.close()
        return traceList

# add specified text to the given file
# OPTIONAL: write the added text to the console as well.
def appendToFile(text):
        with open(filePath, "a") as file:
                file.write(text + "\n")
        #print("Added to file: " + text.strip())

#Sort trace by the component is is "attached" to
def sortTrace(trace, lower_time, upper_time):
        sortedTrace = []
        y = sorted(trace, key = lambda x: float(x[0]))
        for item in y:
                time = float(item[0])
                if not((time) < float(lower_time) or (time) > float(upper_time)):
                        sortedTrace.append(item)
        return sortedTrace

# if the trace for the "next" module is empty, create the new module.
# if the current trace entry is the same module as the one currently saved, add this to the module aswell
def addModules(trace, component):
        i = 1
        moduleTrace = []
        while i < len(trace):
                current = trace[i][2].split("_")[0]
                if current == component:
                        moduleTrace.append(trace[i])
                i = i + 1
        create_model(moduleTrace)


def create_model(trace):
        #Save all unique components in a list
        i = 0
        comp_list = []
        while i < len(trace):
                comp = trace[i][2].split("=")[0]
                value = trace[i][2].split("=")[1]
                if not comp in comp_list:
                        comp_list.append(comp)
                i = i + 1

        #Write each VAR and all its possible values
        comp_dict = find_all_values(comp_list, trace)
        if stage == "var":
                append_all_variables(comp_dict)

        #Write each 'initial' value for every VAR
        elif stage == "init":
                for comp in comp_dict:
                        appendToFile("\t\tinit(" + comp + "):=" + comp_dict[comp][0] + ";")

        #Write all transition conditions for every VAR
        elif stage == "next":
                find_and_print_transitions(comp_dict, trace)

#write each VAR and its possible states, in order of appearence.(inital value first, then in order of appearence)
def append_all_variables(comp_dict):
        for comp in comp_dict:
                i = 0
                text = "\t\t" + comp + ": {"
                while i < len(comp_dict[comp]):
                        text = text + comp_dict[comp][i] + ","
                        i = i + 1
                text = text[:-1] + " };"
                if "FALSE" in text or "TRUE" in text:
                        appendToFile("\t\t" + comp + ": boolean;")
                else:
                        appendToFile(text)
                        
#get the initial value for the current component, as well as ALL its other possible values        
def find_all_values(comp_list, trace):
        comp_dict = {}
        for component in comp_list:
                value_list = [initial_values[component]]
                i = 0
                while i < len(trace):
                        if component == trace[i][2].split("=")[0] and trace[i][2].split("=")[-1] not in value_list:
                                value_list.append(trace[i][2].split("=")[-1])
                        i = i + 1
                comp_dict[component] = value_list
        return comp_dict
                
#write each variables transition cases, but with only components that are DIRECTLY related.
def find_and_print_transitions(comp_dict, trace):
        for component in comp_dict:
                i = 0
                addedconstraints = []
                appendToFile("\t\tnext(" + component + ") := case")
                while i < len(trace):
                        text = ""
                        for item in initial_values:
                                if component.split("_")[0] in item:
                                        text = text + "(" + item + "=" + initial_values[item] + ") & "
                        initial_values[trace[i][2].split("=")[0]] = trace[i][2].split("=")[-1]
                        text = text[:-2] + ":" + initial_values[component] + ";"

                        notAllowed = component + "=" + initial_values[component]
                        if text not in addedconstraints and notAllowed not in text:
                                appendToFile("\t\t\t" + text)
                                addedconstraints.append(text)
                        if "in_motion" in initial_values[component]:
                                j = i + 1
                                detected = False
                                if component in trace[i][2]:
                                        while j < len(trace):
                                                if trace[j][2].split("=")[0] == component and not detected:
                                                        if "in_motion" in trace[i][2]:
                                                                text = ("(" + trace[i][2] + "): ")
                                                                text = text + trace[j][2].split("=")[-1] + ";"
                                                                detected = True
                                                j = j + 1
                                if text not in addedconstraints:
                                        appendToFile("\t\t\t" + text)
                                        addedconstraints.append(text)
                        i = i + 1
                sm_dict[component] = addedconstraints
                appendToFile("\t\t\tTRUE: " + component + ";")
                appendToFile("\t\tesac;")

#use dictionary to save all values. It's easy to overwrite them with newer values.
def addInitial_values():
        f = open("initial_values.txt", "r")
        varDict = {}
        for line in f:
                line = line.split(";")[0]
                line = line.split(":")
                varDict[line[0]] = line[1]
        f.close()
        return varDict

def generate_data(trace, component):
        sDict = {}
        #Dependency list for they paths taken in the state machine
        depList = []
        order = 0
        for line in trace:
                sList = []
                order = order + 1
                for line2 in initial_values:
                        if component in line2:
                                text = line2 + "=" + initial_values[line2]
                                sList.append(text)
                sDict[str(order)] = sList
                initial_values[line[2].split("=")[0]] = line[2].split("=")[1]

        #Adds the dependencies for each of the state transitions
        for stateNumber in sDict:
                depList.append(stateNumber)
                for stateNumber_check in sDict:
                        #replace the linear dependencies if an already existing state exists
                        if (stateNumber_check < stateNumber) and (sDict[stateNumber] == sDict[stateNumber_check]):
                                depList.pop(-1)
                                depList.append(stateNumber_check)


        #Write all the transitions and to where they go. note that multiple states that are visited from several locations are
        # multiplied when displaying them through PlantUML.
        i = 1
        while i <= len(depList):
                for constraint in sDict[str(i)]:
                        writeToUmlfile("State" + depList[i-1] + " : " + constraint)
                if i == len(depList):
                        writeToUmlfile("State" + depList[-1] + " --> State" + depList[0])
                else:
                        writeToUmlfile("State" + depList[i-1] + " --> State" + depList[i])
                i = i + 1

                

def getFile():
        return "C:\\Users\\JohannesWIN10\\Documents\\nxtSTUDIO\\EnAS 2020 VC with Skills\\NuSMV_Models\\" + getTime()

def writeToUmlfile(text):
        with open("C:\\Users\\JohannesWIN10\\Documents\\nxtSTUDIO\\EnAS 2020 VC with Skills\\PlantUML_StateMachines\\uml.txt", "a") as file:
                file.write(text + "\n")

### variables
# name/location of read file and name/location to save the new file
activeTrace = "2020_11_6_11_58_trace_log.txt"
filePath = "C:\\Users\\JohannesWIN10\\Documents\\nxtSTUDIO\\EnAS 2020 VC with Skills\\GeneratedTraces\\" + getTime() + "_log.smv"
initial_values = addInitial_values()

#Make sure that the stages are generated in the correct sequence. The entire VAR section needs to be done before the INIT section can be created. the same goes for NEXT.
#The sections for AGV, IRB, C1 etc. also needs to be of the correct sequence.
stage = ["var", "init", "next"]
components = ["AGV", "IRB", "C1", "C2", "C3", "C4", "C5", "C6"]
sm_dict = {}

## between what time in the trace that is explored. Use 0 and 3600 to get an hour
lowerTime = 2
upperTime = 3600

trace_data = sortTrace(readFile(activeTrace), lowerTime, upperTime)

appendToFile("MODULE main")
appendToFile("\tVAR")
stage = "var"
i = 0
while i < len(components):
        addModules(trace_data, components[i])
        i = i + 1
appendToFile("")

appendToFile("\tASSIGN")
stage = "init"
i = 0
while i < len(components):
        addModules(trace_data, components[i])
        i = i + 1

stage = "next"
i = 0
while i < len(components):
        appendToFile("-----" + components[i])
        addModules(trace_data, components[i])
        i = i + 1

writeToUmlfile("@startuml")
writeToUmlfile("[*] --> State1")
i = 0
while i < len(components):
        subsystem_trace = []
        j = 0
        while j < len(trace_data):
                if trace_data[j][2].split("_")[0] == components[i]:
                        subsystem_trace.append(trace_data[j])
                j = j + 1
        generate_data(subsystem_trace, components[i])
        i = i + 1
writeToUmlfile("@enduml")

