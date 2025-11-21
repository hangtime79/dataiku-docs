import nltk

text = '''
Dataiku integrates with your existing infrastructure — on-premises or in the cloud. It takes advantage of 
each technology’s native storage and computational layers. Additionally, Dataiku provides 
a fully hosted SaaS option built for the modern cloud data stack. With fully 
managed elastic AI powered by Spark and Kubernetes, you can achieve maximum performance 
and efficiency on large workloads.
'''

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
print('\n-----\n'.join(sent_detector.tokenize(text.replace('\n', ' ').strip())))
