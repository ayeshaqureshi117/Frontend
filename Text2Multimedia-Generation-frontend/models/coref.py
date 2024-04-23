import sys
sys.path.append('fast-coref/src')
from inference.model_inference import Inference
from copy import deepcopy

!gdown --id 1c_X-iDJNr4BM9iAN4YjUMVJUS741eA_Z
inference_model = Inference("./", encoder_name="shtoshni/longformer_coreference_joint")

def coref_mapping(sentence):
  
  output = inference_model.perform_coreference(sentence)
  tokens = deepcopy(output['tokenized_doc']['orig_tokens'])
  sub_tokens = deepcopy(output['tokenized_doc']['subtoken_map'])
  newMapped = deepcopy(output['tokenized_doc']['orig_tokens'])
  indx = []
  for cluster in output["clusters"]:
      init_mention = cluster[0][1]
      if len(cluster) > 1:
        temp = []
        for (start, end), mention in cluster:
            s = len(set(sub_tokens[:(start)+1]))-1
            e = len(set(sub_tokens[:(end)+1]))
            indx.append(((s,e),init_mention))
            temp.append((tokens[s:e], mention))
    newMapped=[]
  check=0
  indx = sorted(indx, key=lambda x: x[0][0])
  i=0
  while(True):
    if i < indx[check][0][0]:
      newMapped.append(tokens[i])
      i+=1
    else:
      newMapped.append(indx[check][1])
      i+=(indx[check][0][1]-indx[check][0][0])
      if check+1!=len(indx):
        check+=1
      else:
        break
  if i<len(tokens)-1:
    for j in range(i,len(tokens)):
      newMapped.append(tokens[j])
  new_prompt = ''
  for i in newMapped:
    new_prompt += i +' '
  return new_prompt