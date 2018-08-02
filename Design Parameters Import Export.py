#Author-rohit.bapat@autodesk.com
#Description-Design Parameters Import/Export

import adsk.core, adsk.fusion, adsk.cam, traceback
import os.path

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
       
        input = '0'
        isCancelled = True
        retVals = ui.inputBox('Import[0] / Export[1]', 'Design Parameters Import-Export', input)
        if retVals[0]:
            (input, isCancelled) = retVals
            
        if not isCancelled and (input == '0' or input == '1'):
            #Import CSV
            if input == '0':
                fileDlg = ui.createFileDialog()
                fileDlg.isMultiSelectEnabled = False
                fileDlg.title = 'Design Parameters Import Dialog'
                fileDlg.filter = '*.*'
                
                # Show file open dialog
                dlgResult = fileDlg.showOpen()
                if dlgResult == adsk.core.DialogResults.DialogOK:
                    file = open(fileDlg.filename,'r')
                    for line in file:
                        line = line.replace(" ", "")
                        paramInputs = line.split(',')
                        if(len(paramInputs) >=3):
                            if(len(paramInputs) ==3):
                                paramInputs.append('')
                            
                            pName = str(paramInputs[0])
                            pExpression = str(paramInputs[1])
                            pUnit = str(paramInputs[2])
                            pComment = str(paramInputs[3])
                            design.userParameters.add(pName,adsk.core.ValueInput.createByString(pExpression),pUnit,pComment)
                        
                    file.close()
            #Export CSV                            
            else:
                fileDlg = ui.createFileDialog()
                fileDlg.isMultiSelectEnabled = False
                fileDlg.title = 'Design Parameters Export Dialog'
                fileDlg.filter = '*.*'
                dlgResult = fileDlg.showSave()
                if dlgResult == adsk.core.DialogResults.DialogOK:   
                    file = open(fileDlg.filename,'w+')
                    for i in range(0,design.allParameters.count):
                        param = design.allParameters.item(i)
                        file.write(str(param.name)+' , '+ str(param.expression)+' , '+ str(param.unit) + ' , ' + str(param.comment) + os.linesep)
                    file.close()
        else:
            ui.messageBox('bad')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
