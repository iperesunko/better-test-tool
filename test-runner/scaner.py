from pprint import pprint
import os


class FilesScaner:
	files = []

	def __init__(self, pref, suff):
		self.pref = pref
		self.suff = suff

	def scan(self, path):
		found_files = os.walk(path)

		for dirpath, _, filenames in found_files:
			for _file in filenames:
				if self.files_filter(_file):
					self.files.append(os.path.join(dirpath, _file))

	def files_filter(self, file):
		if file.startswith(self.pref) and file.endswith(self.suff):
			return True

		return False
	
	def show_files(self):
		pprint(self.files)

def main():
	test = FilesScaner('test_', '.py')
	test.scan('vano_test/saleor/tests')
	test.show_files()

if __name__ == '__main__':
	main()