
console.log("DataEntry Platform ready");

function openRecordModal(item=null){
  const form=document.getElementById('recordForm');
  const title=document.getElementById('recordModalTitle');
  const save=document.getElementById('recordSaveBtn');
  const del=document.getElementById('recordDeleteBtn');
  form.action=item ? `/records/${item.id}/update` : '/records/create';
  title.textContent=item ? 'Edit Record' : 'New Record';
  save.textContent=item ? 'Update' : 'Save';
  del.classList.toggle('d-none', !item);
  document.getElementById('record_id').value=item?.id || '';
  document.getElementById('ref_no').value=item?.ref_no || '';
  document.getElementById('title').value=item?.title || '';
  document.getElementById('category').value=item?.category || '';
  document.getElementById('priority').value=item?.priority || 'medium';
  document.getElementById('status').value=item?.status || 'draft';
  document.getElementById('owner').value=item?.owner || '';
  document.getElementById('due_date').value=item?.due_date || '';
  del.onclick = ()=>{ if(confirm('Delete this record?')) fetch(`/records/${item.id}/delete`, {method:'POST'}).then(()=>location.reload()); };
}
function openUserModal(item=null){
  const form=document.getElementById('userForm');
  const title=document.getElementById('userModalTitle');
  const save=document.getElementById('userSaveBtn');
  const del=document.getElementById('userDeleteBtn');
  form.action=item ? `/users/${item.id}/update` : '/users/create';
  title.textContent=item ? 'Edit User' : 'New User';
  save.textContent=item ? 'Update' : 'Save';
  del.classList.toggle('d-none', !item);
  document.getElementById('user_id').value=item?.id || '';
  document.getElementById('full_name').value=item?.full_name || '';
  document.getElementById('user_email').value=item?.email || '';
  document.getElementById('role').value=item?.role || 'user';
  document.getElementById('user_status').value=item?.status || 'active';
  del.onclick = ()=>{ if(confirm('Delete this user?')) fetch(`/users/${item.id}/delete`, {method:'POST'}).then(()=>location.reload()); };
}
