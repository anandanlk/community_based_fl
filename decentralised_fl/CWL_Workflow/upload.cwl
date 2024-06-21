cwlVersion: v1.2
class: CommandLineTool

requirements: 
  InlineJavascriptRequirement: {}
  
inputs:
  file_path2:
    type: File?
  aggregator_upload_url:
    type: string
  round:
    type: string

baseCommand: curl

arguments:
  - -F 
  - 'file=@$(inputs.file_path2.path)' 
  -  $(inputs.aggregator_upload_url.split('/').slice(0, -1).concat([inputs.round, 'upload_weights']).join('/'))
outputs:
  upload_state: stdout

stdout: upload.txt