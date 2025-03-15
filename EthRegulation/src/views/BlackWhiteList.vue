const rules = {
  address: [
    { required: true, message: '请输入账户地址', trigger: 'blur' },
    { pattern: /^0x[0-9a-fA-F]{40}$/, message: '请输入正确的以太坊账户地址', trigger: 'blur' }
  ],
  operator: [
    { required: true, message: '请选择操作人', trigger: 'change' },
    { validator: validateOperator, trigger: 'change' }  // 添加后端对应的验证
  ],
  type: [
    { required: true, message: '请选择类型', trigger: 'change' },
    { type: 'number', min: 1, max: 2, message: '类型只能是1或2', trigger: 'change' }
  ],
  organization: [
    { required: true, message: '请选择发布机构', trigger: 'change' },
    { validator: validateOrganization, trigger: 'change' }  // 添加后端对应的验证
  ],
  region: [
    { required: true, message: '请选择使用范围', trigger: 'change' },
    { validator: validateRegion, trigger: 'change' }  // 添加后端对应的验证
  ]
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    const res = form.value.id 
      ? await updateItem(form.value.id, form.value)
      : await addItem(form.value)

    if (res.code === 200) {
      ElMessage.success(form.value.id ? '更新成功' : '添加成功')
      dialogVisible.value = false
      await fetchData()  // 刷新列表
    } else {
      // 处理后端返回的具体错误信息
      if ('errors' in res) {
        const errorMsg = Object.values(res.errors).flat().join(', ')
        ElMessage.error(errorMsg || res.message)
      } else {
        ElMessage.error(res.message)
      }
    }
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败，请重试')
  }
}