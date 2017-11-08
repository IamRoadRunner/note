def ExportView(request):
    objs = EventDetail.objects.all()
    if objs:
        sheet = Workbook(encoding='utf-8')
        s = sheet.add_sheet('数据表')
        s.write(0, 0, '楼栋')
        s.write(0, 1, '单元')
        s.write(0, 2, '楼层')
        s.write(0, 3, '房号')
        s.write(0, 4, '原价')
        s.write(0, 5, '线上总价')
        row=1
        for obj in objs:
            building = obj.building
            unit = obj.unit
            floor = obj.floor
            room_num = obj.room_num
            price = obj.price
            total = obj.total
            s.write(row, 0, building)
            s.write(row, 1, unit)
            s.write(row, 2, floor)
            s.write(row, 3, room_num)
            s.write(row, 4, price)
            s.write(row, 5, total)
            row+=1
        sio=BytesIO()
        sheet.save(sio)
        sio.seek(0)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename=export.xls'
        response.write(sio.getvalue())
        return response
    return JsonResponse({'msg': '内容为空！'})
