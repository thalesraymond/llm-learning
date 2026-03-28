from functions.get_files_info import get_files_info


try:
  print("Result for current directory:")
  print(get_files_info("calculator"))
except Exception as e:
  print(e)


try:
  print("Result for current directory:")
  print(get_files_info("calculator", "pkg"))
except Exception as e:
  print(e)


try:
  print("Result for current directory:")
  print(get_files_info("calculator", "/bin"))
except Exception as e:
  print(e)


try:
  print("Result for current directory:")
  print(get_files_info("calculator", "../"))
except Exception as e:
  print(e)





