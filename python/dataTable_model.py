from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class dataTableModel(QAbstractTableModel):
    def __init__(self, data_in, header_in, maxNumRows=20,parent=None):
        super(dataTableModel, self).__init__()
        #QAbstractTableModel.__init__(self, parent)
        self.array_data = data_in
        self.header_data = header_in
        self.maxNumRows = maxNumRows
        #self.setLayoutDirection()

    def rowCount(self,parent):
        return len(self.array_data)

    def columnCount(self, parent):
        if len(self.array_data) > 0:
            return len(self.array_data[0])
        return 0

    def data(self,index,role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            if role == Qt.TextAlignmentRole:
                return Qt.AlignCenter | Qt.AlignVCenter
            return QVariant()
        return QVariant(self.array_data[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.header_data[col])
        return QVariant()

    def removeRows(self, position, rows=1, index=QModelIndex()):
        print "\n\t\t ...removeRows() Starting position: '%s'"%position, 'with the total rows to be deleted: ', rows
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        #self.items = self.items[:position] + self.items[position + rows:]
        self.array_data = self.array_data[:position] + self.array_data[position + rows:]
        self.endRemoveRows()

        return True

    def insertRows(self, position, rows=1, index=QModelIndex()):
        print "\n\t\t ...insertRows() Starting position: '%s'"%position, 'with the total rows to be inserted: ', rows
        indexSelected=self.index(position, 0)
        itemSelected=indexSelected.data().toPyObject()

        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.array_data.insert(position + row,  "%s_%s"% (itemSelected, self.added))
            self.added+=1
        self.endInsertRows()
        return True
