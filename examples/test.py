#  Copyright (c) 2020. Davi Pereira dos Santos
#      This file is part of the kururu project.
#      Please respect the license. Removing authorship by any means
#      (by code make up or closing the sources) or ignoring property rights
#      is a crime and is unethical regarding the effort and time spent here.
#      Relevant employers or funding agencies will be notified accordingly.
#
#      kururu is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      kururu is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with kururu.  If not, see <http://www.gnu.org/licenses/>.
#

from aiuna.file import File
from cruipto.uuid import UUID
from kururu.tool.dataflow.autoins import AutoIns
from kururu.tool.dataflow.delin import DelIn
from kururu.tool.enhancement.pca import PCA1
from kururu.tool.evaluation.metric import Metric2, Metric
from kururu.tool.evaluation.partition import Partition
from kururu.tool.evaluation.split import Split
from kururu.tool.learning.supervised.classification.svm import SVM2, SVM
from kururu.tool.manipulation.slice import Slice
from transf._ins import Ins

print(File("iris.arff").data)
wf = File("iris.arff") * Split(mode="holdout") * SVM2() * Metric2()
data4 = wf.data
print("met", data4.r, data4.inner.r)

data = File("iris.arff").data
print(data.X[:2], data.y[:2])

split = Split(mode="holdout")
print(11111, data.id, data.inner)
data2 = split << data
print(22222, data2.id, data2.inner.id)
print(data2.X[:2], data2.y[:2])

svm = SVM2()
data3 = svm << data2
print("svm", data3.y[:2], data3.z[:2])

met = Metric2()
data4 = met << data3
data = svm(data) << data
met = Metric()
result = met << data
print(svm)

print("iris", data.id)
print("iden", UUID.identity)

print("default p/ treinar depois com data externo:  SVM()(inner)")
svm = SVM()
data = data >> DelIn
r = svm(data).process(data)
print("svm\t\t", svm.id)
print("svm(data)\t", svm(data).id)
print("inner*svm\t", Ins(data).uuid * svm.uuid)
print("data*inner*svm", data.uuid * Ins(data).uuid * svm.uuid)
print(r.id + "\n")

print("default treinado:  SVM(inner)")
model = SVM(data)
r = model.process(data)
print("svm\t\t", svm.id)
print("model\t", model.id)
print("inner\t", Ins(data).uuid)
print("inner*svm\t", Ins(data).uuid * SVM().uuid)
print("data*inner*svm", data.uuid * Ins(data).uuid * SVM().uuid)
print(r.id + "\n")

print("default p/ treinar depois com data interno:  SVM() + data.inner")
print("svm\t\t", svm.uuid)
data2 = AutoIns().process(data)
data = data2
print("data com inner\t", data.id)
print("data*svm", data.uuid * svm.uuid)
svm = SVM2()

r = svm.process(data)
print(r.id + "\n", r.history)
print("***********************************************")

print()
print("---------------------------")
print()
data = File("iris.arff").data

print("PCA()(inner)")
data = data >> DelIn
pca = PCA1()
r = pca(data).process(data)
print(r.uuid.__str__() + "\n")

print("PCA(inner)")
pca = PCA1(data)
r = pca.process(data)
print(r.uuid.__str__() + "\n")

print("PCA() + data.inner")
pca = PCA1()
data = data >> AutoIns
r = pca.process(data)
print(r.uuid.__str__() + "\n")
data = data >> DelIn

print("PCA\t\t", pca.uuid)
print("PCA*data\t", pca.uuid(data.uuid))
print("data*PCA*data", data.uuid * pca.uuid(data.uuid))
print(r.uuid)

print()
print("---------------------------")
print()

print("Split()")
data = data >> DelIn
split = Split()
r = split.process(data)
print(r.uuid.__str__() + "\n")

print("Split() + data.inner")
split = Split()
r = split.process(data)
print(r.uuid.__str__() + "\n")

print("Split\t\t", split.uuid)
print("Split*data\t", split.uuid(data.uuid))
print("data*Split*data", data.uuid * split.uuid(data.uuid))
print(r.uuid)

print()
print("---------------------------")
print()

print("Partition()")
data = data >> DelIn
partition = Partition()
r = partition.process(data)
print(r.uuid.__str__() + "\n")

print("Partition() + data.inner")
partition = Partition()
data = data >> AutoIns
r = partition.process(data)
print(r.uuid.__str__() + "\n")

print("Partition\t\t", partition.uuid)
print("Partition*data\t", partition.uuid(data.uuid))
print("data*Partition*data", data.uuid * partition.uuid(data.uuid))
print(r.uuid)

r = PCA1 * SVM
print(type(r), r)

data = data >> DelIn
d = (SVM(data) * Slice()).process(data)
print(d.X)
print(d.history)

print(PCA1.sample())

import numpy as np

np.random.seed(2)
p = PCA1(data, n=2).sample()
print(p, data.X.shape[1])
d = p << data
tr = d.inner
print(data.id, "inner                    ", tr and tr.id, "!!!!!!!!!!!!!", d.failure, "        ", d.id)
# print((PCA * SVM).sample().process(data))

print("vvvvvvvvvvvvvvvvvvvvvvvvvvvv")
# TODO: imprimir stacktrace no log de saida
