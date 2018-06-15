//index.js
//获取应用实例
const app = getApp()
const url = "https://wxapi.yangruixin.com/query";
const picInterface = "https://wx.idsbllp.cn/game/cet/smallApp.php";
Page({
  data: {
    id: "",
    name: "",
    grade: {},
    recognizeId: "",
    recognizeName: "",
    loading: 0,
  },
  nameInput: function (e) {
    this.setData({
      name: e.detail.value
    })
  },
  idInput: function (e) {
    this.setData({
      id: e.detail.value
    })
  },
  //事件处理函数
  getUserScore: function (e) {
    var json = "";
    var that = this;
    if (that.data.loading == 0) {
      wx.showLoading({
        title: '查询中',
      })
    }
    console.log(this.data.id.length)
    if (this.data.id.length != 15) {
      wx.showModal({
        title: "输入错误！",
        content: "准考证号长度不是15位，再试试吧",
        success: function (res) {
          if (res.confirm) {
            console.log('用户点击确定')
          } else if (res.cancel) {
            console.log('用户点击取消')
          }
        }
      })
      if (that.data.loading == 0) {
        wx.hideLoading()
      } else {
        wx.stopPullDownRefresh()
      }
    } else {
      wx.request({
        url: url, //仅为示例，并非真实的接口地址
        method: "post",
        data: {
          name: this.data.name,
          id: this.data.id,
          // name: "杨瑞鑫",
          // id: "508160172203827",
        },
        header: {
          'content-type': 'application/x-www-form-urlencoded'
        },
        success: function (res) {
          json = res.data;
          if (json.status == 200) {
            that.setData({
              grade: json.data
            });

            wx.redirectTo({
              url: '../grade/grade?id=' + json.data.id + '&name=' + json.data.name + "&sum=" + json.data.sum + "&listen=" + json.data.listen + "&read=" + json.data.read + "&write=" + json.data.write,
            })
          }
          else if (json.info.indexOf("error") >= 0 && json.status == 500) {
            wx.showModal({
              title: "服务器错误",
              content: "好像没能成功拿到数据呢，再试一次试试？",
              success: function (res) {
                if (res.confirm) {
                  console.log('用户点击确定')
                } else if (res.cancel) {
                  console.log('用户点击取消')
                }
              }
            })
          }
          else {
            wx.showModal({
              title: "请求错误",
              content: "请检查准考证号姓名是否输入错误",
              success: function (res) {
                if (res.confirm) {
                  console.log('用户点击确定')
                } else if (res.cancel) {
                  console.log('用户点击取消')
                }
              }
            })
          }
        },
        complete: function () {
          if (that.data.loading == 0) {
            wx.hideLoading()
          } else {
            wx.stopPullDownRefresh()
          }
        }
      })
    }
  },
  getLocalPicture: function (e) {
    var that = this;
    wx.chooseImage({
      success: function (res) {
        if (that.data.loading == 0) {
          wx.showLoading({
            title: '上传中',
          })
        }
        var tempFilePaths = res.tempFilePaths;
        wx.uploadFile({
          url: picInterface,
          filePath: tempFilePaths[0],
          name: 'picture',
          formData: {
            'openid': 'test',
          },
          success: function (res) {
            var data = res.data
            var json = JSON.parse(data);
            console.log(json);
            that.setData({
              recognizeId: json.data.examID,
              recognizeName: json.data.name,
              id: json.data.examID,
              name: json.data.name,
            })
          },
        })
      },
      complete: function () {
        if (that.data.loading == 0) {
          wx.hideLoading()
        } else {
          wx.stopPullDownRefresh()
        }
      }
    })
  },
})
